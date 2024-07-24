import streamlit as st
from candidateRanking import rank_and_filter_candidates

def main():
    st.title("Hire'em | Help you finding the best")

    # Required skills
    st.subheader("Required Skills")
    col1, col2 = st.columns([3, 1])
    with col1:
        required_skills = st.text_input("Required Skills")
    with col2:
        required_skills_weight = st.number_input("Weight for Req. Skills", min_value=0.0, max_value=10.0, step=0.1)

    # Desired skills
    st.subheader("Desired Skills")
    col3, col4 = st.columns([3, 1])
    with col3:
        desired_skills = st.text_input("Desired Skills")
    with col4:
        desired_skills_weight = st.number_input("Weight for Desired Skills", min_value=0.0, max_value=10.0, step=0.1)

    # Experience
    st.subheader("Experience")
    col5, col6 = st.columns([3, 1])
    with col5:
        experience = st.slider("Years", min_value=0, max_value=30, value=(0, 5))
    with col6:
        experience_weight = st.number_input("Weight for Experience", min_value=0.0, max_value=10.0, step=0.1)

    # Highest Qualification
    st.subheader("Highest Qualification")
    col7, col8 = st.columns([3, 1])
    with col7:
        qualifications = ["High School", "Associate Degree", "Bachelor's Degree", "Master's Degree", "PhD"]
        highest_qualification = st.selectbox("Qualification", qualifications)
    with col8:
        highest_qualification_weight = st.number_input("Weight for Qualification", min_value=0.0, max_value=10.0, step=0.1)

    # College
    st.subheader("College")
    col9, col10 = st.columns([3, 1])
    with col9:
        college = st.text_input("College")
    with col10:
        college_weight = st.number_input("Weight for College", min_value=0.0, max_value=10.0, step=0.1)

    # Company
    st.subheader("Company")
    col11, col12 = st.columns([3, 1])
    with col11:
        company = st.text_input("Company")
    with col12:
        company_weight = st.number_input("Weight for Company", min_value=0.0, max_value=10.0, step=0.1)

    # Company Domain
    st.subheader("Company Domain")
    company_domain = st.text_input("Domain")

    if st.button("Submit"):
        st.write("Form Submitted with the following data:")
        st.write("Required Skills:", required_skills, "| Weight:", required_skills_weight)
        st.write("Desired Skills:", desired_skills, "| Weight:", desired_skills_weight)
        st.write("Experience:", experience, "| Weight:", experience_weight)
        st.write("Highest Qualification:", highest_qualification, "| Weight:", highest_qualification_weight)
        st.write("College:", college, "| Weight:", college_weight)
        st.write("Company:", company, "| Weight:", company_weight)
        st.write("Company Domain:", company_domain)

        ranked_candidates = rank_and_filter_candidates(
            required_skills, required_skills_weight,
            desired_skills, desired_skills_weight,
            experience, experience_weight,
            highest_qualification, highest_qualification_weight,
            college, college_weight,
            company, company_weight,
            company_domain
        )
        
        st.write("---")
        st.write(f"Found {len(ranked_candidates)} candidates")
        st.write("---")

        for candidate in ranked_candidates:
            candidate_info = candidate["_source"]
            st.write("Name:", candidate_info.get("Name", "N/A"))
            st.write("Skills:", ", ".join(candidate_info.get("Skills", [])))
            st.write("Experience:", candidate_info.get("Year of Experience", "N/A"))
            st.write("Highest Qualification:", candidate_info.get("Highest Qualification", "N/A"))
            st.write("College:", ", ".join(college["College Name"] for college in candidate_info.get("Colleges", [])))
            st.write("Companies:", ", ".join(candidate_info.get("Companies", [])))
            st.write("---")

if __name__ == "__main__":
    main()