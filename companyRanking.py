from elasticsearch import Elasticsearch

# Initialize Elasticsearch
es = Elasticsearch("http://65.2.188.173:9200/")

#--------------------------------------------------------------------------------------------------------#
# Define hardcoded weights for ranking
weights = {
    "year_of_establishment": 0.3,
    "company_size": 0.4,
    "revenue": 0.3
    }

#--------------------------------------------------------------------------------------------------------#
def find_similar_companies(domain):
    # Elasticsearch query to find companies by domain
    query = {
        "query": {
            "match": {
                "Domain": domain
            }
        }
    }

    # Perform the search
    response = es.search(index="companies", body=query)
    return response["hits"]["hits"]

#--------------------------------------------------------------------------------------------------------#
def rank_companies(companies):
    def rank_score(company):
        year = company["_source"].get("year_of_establishment", 0)
        size = company["_source"].get("company_size", 0)
        revenue = company["_source"].get("revenue", 0)

        score = (year * weights["year_of_establishment"] +
                 size * weights["company_size"] +
                 revenue * weights["revenue"])
        return score

    # Sort companies based on the computed rank score
    ranked_companies = sorted(companies, key=rank_score, reverse=True)
    return ranked_companies

#--------------------------------------------------------------------------------------------------------#
def get_ranked_companies(domain):
    similar_companies = find_similar_companies(domain)
    ranked_companies = rank_companies(similar_companies)
    return ranked_companies

#--------------------------------------------------------------------------------------------------------#
