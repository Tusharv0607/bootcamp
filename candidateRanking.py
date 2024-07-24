from elasticsearch import Elasticsearch
from companyRanking import get_ranked_companies

# Initialize Elasticsearch
es = Elasticsearch("http://65.2.188.173:9200/")

#--------------------------------------------------------------------------------------------------------#
# Function to fetch the ranking of the entered college
def fetch_college_rank(college_name):
    response = es.search(index="colleges", body={
        "query": {
            "match": {
                "College Name": college_name
            }
        }
    })
    hits = response['hits']['hits']
    if hits:
        return hits[0]['_source']['College Ranking']
    return None

#--------------------------------------------------------------------------------------------------------#
def rank_and_filter_candidates(required_skills, required_skills_weight,
                                desired_skills, desired_skills_weight,
                                experience_range, experience_weight,
                                highest_qualification, highest_qualification_weight,
                                college, college_weight,
                                company, company_weight,
                                company_domain):
    
    ranked_companies = []

    if(company_domain):
        ranked_companies = get_ranked_companies(company_domain)
   
    ranked_company_names = [company["_source"].get("C_Name", "N/A") for company in ranked_companies]

    # Define the query to search for candidates
    query = {
        "query": {
            "bool": {
                "must": [],
                "filter": [],
                "should": [],
                "must_not": []
            }
        }
    }

    # Required Skills
    if required_skills:
        skills_list = [skill.strip() for skill in required_skills.split(',')]
        query["query"]["bool"]["must"].append({
            "terms": {
                "Skills": skills_list
            }
        })
    
    # Desired Skills
    if desired_skills:
        skills_list = [skill.strip() for skill in desired_skills.split(',')]
        query["query"]["bool"]["should"].append({
            "terms": {
                "Skills": skills_list
            }
        })

    # Experience
    if experience_range:
        query["query"]["bool"]["filter"].append({
            "range": {
                "Year of Experience": {
                    "gte": experience_range[0],
                    "lte": experience_range[1]
                }
            }
        })

    # Highest Qualification
    if highest_qualification:
        qualification_map = {
            "High School": 1,
            "Associate Degree": 2,
            "Bachelor's Degree": 3,
            "Master's Degree": 4,
            "PhD": 5
        }
        
        # Get the numeric level for the provided highest qualification
        level = qualification_map.get(highest_qualification)
        
        # If level is found in the map
        if level:
            # Use a should clause to include candidates with the given qualification or any higher qualification
            query["query"]["bool"]["must"].append({
                "terms": {
                    "Highest Qualification": [
                        # Include all qualifications with numeric value >= the given level
                        key for key, value in qualification_map.items() if value >= level
                    ]
                }
            })

    # College Ranking Filter
    if college:
        college_rank = fetch_college_rank(college)
        if college_rank is not None:
            query["query"]["bool"]["must"].append({
                "range": {
                    "Colleges.College Ranking": {
                        "gte": college_rank - 5,
                        "lte": college_rank + 5
                    }
                }
            })

    # Company
    if company:
        query["query"]["bool"]["filter"].append({
            "terms": {
                "Companies": ranked_company_names
            }
        })

    # Perform the search
    response = es.search(index="candidate_profile", body=query)
    candidates = response["hits"]["hits"]

    # Rank the candidates
    def rank_score(candidate):
        source = candidate["_source"]
        skills = set(source.get("Skills", []))
        company = source.get("Companies", [])
        colleges = source.get("Colleges", [])

        required_skill_score = len(set(required_skills.split(",")).intersection(skills)) * required_skills_weight

        desired_skill_score = len(set(desired_skills.split(",")).intersection(skills)) * desired_skills_weight

        experience_score = source.get("Year of Experience", 0) * experience_weight

        qualification_score = highest_qualification_weight if source.get("Highest Qualification") == highest_qualification else 0

        company_score = company_weight if any(comp in ranked_company_names for comp in company) else 0

        college_score = 0
        target_college_rank = fetch_college_rank(college)

        if target_college_rank:
            for clg in colleges:
                college_rank = clg.get("College Ranking")
                if college_rank:
                    if abs(college_rank - target_college_rank) <= 5:
                        college_score += (5 - abs(college_rank - target_college_rank)) * college_weight

        total_score = (required_skill_score + desired_skill_score +
                       experience_score + qualification_score +
                       company_score + college_score)

        return total_score

    ranked_candidates = sorted(candidates, key=rank_score, reverse=True)

    return ranked_candidates
#--------------------------------------------------------------------------------------------------------#
