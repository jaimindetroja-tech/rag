"""
Comprehensive Test Cases for Internal Expertise Finder
Based on real data from profiles.json

Run these tests to verify the application works correctly.
Compare actual output with expected output listed in test_expected_outputs.md
"""

import sys
sys.path.append('..')

from data_processing import (
    load_profiles_from_json,
    convert_profiles_to_documents,
    extract_project_information,
    create_document_content
)
from indexing import create_vector_index, get_unique_metadata_values
from config import DATA_PATH


def test_1_load_profiles():
    """Test Case 1: Load profiles from JSON"""
    print("=" * 70)
    print("TEST 1: Load Profiles from JSON")
    print("=" * 70)
    
    profiles = load_profiles_from_json(DATA_PATH)
    
    print(f"✓ Total profiles loaded: {len(profiles)}")
    print(f"✓ First profile name: {profiles[0]['name']}")
    print(f"✓ First profile team: {profiles[0]['team']}")
    print(f"✓ First profile location: {profiles[0]['location']}")
    print(f"✓ First profile skills count: {len(profiles[0]['skills'])}")
    print(f"✓ Sample skills: {', '.join(profiles[0]['skills'][:5])}")
    
    return profiles


def test_2_extract_project_info():
    """Test Case 2: Extract project information"""
    print("\n" + "=" * 70)
    print("TEST 2: Extract Project Information")
    print("=" * 70)
    
    profiles = load_profiles_from_json(DATA_PATH)
    first_profile = profiles[0]
    
    projects = first_profile.get('projects', [])
    project_details, project_names, project_stacks = extract_project_information(projects)
    
    print(f"✓ Number of projects: {len(project_details)}")
    print(f"✓ Project names: {', '.join(project_names)}")
    print(f"✓ Total unique tech stack items: {len(set(project_stacks))}")
    print(f"✓ Sample tech stack: {', '.join(list(set(project_stacks))[:5])}")
    
    if project_details:
        print(f"\n✓ First project formatted output:")
        print(project_details[0])
    
    return project_details, project_names, project_stacks


def test_3_create_document_content():
    """Test Case 3: Create document content from profile"""
    print("\n" + "=" * 70)
    print("TEST 3: Create Document Content")
    print("=" * 70)
    
    profiles = load_profiles_from_json(DATA_PATH)
    first_profile = profiles[0]
    
    text_content, metadata = create_document_content(first_profile)
    
    print(f"✓ Document text length: {len(text_content)} characters")
    print(f"✓ Metadata keys: {', '.join(metadata.keys())}")
    print(f"✓ Metadata name: {metadata['name']}")
    print(f"✓ Metadata team: {metadata['team']}")
    print(f"✓ Metadata location: {metadata['location']}")
    
    print(f"\n✓ First 500 characters of document:")
    print(text_content[:500])
    
    return text_content, metadata


def test_4_convert_to_documents():
    """Test Case 4: Convert all profiles to documents"""
    print("\n" + "=" * 70)
    print("TEST 4: Convert Profiles to Documents")
    print("=" * 70)
    
    profiles = load_profiles_from_json(DATA_PATH)
    documents = convert_profiles_to_documents(profiles)
    
    print(f"✓ Total documents created: {len(documents)}")
    print(f"✓ First document ID: {documents[0].doc_id}")
    print(f"✓ First document has metadata: {len(documents[0].metadata)} fields")
    print(f"✓ First document text length: {len(documents[0].text)} characters")
    
    # Check all documents have required metadata
    all_have_name = all('name' in doc.metadata for doc in documents)
    all_have_team = all('team' in doc.metadata for doc in documents)
    all_have_location = all('location' in doc.metadata for doc in documents)
    
    print(f"✓ All documents have 'name' metadata: {all_have_name}")
    print(f"✓ All documents have 'team' metadata: {all_have_team}")
    print(f"✓ All documents have 'location' metadata: {all_have_location}")
    
    return documents


def test_5_unique_locations_and_teams():
    """Test Case 5: Extract unique locations and teams"""
    print("\n" + "=" * 70)
    print("TEST 5: Extract Unique Metadata Values")
    print("=" * 70)
    
    profiles = load_profiles_from_json(DATA_PATH)
    
    # Manually extract unique values
    locations = sorted(list(set(p['location'] for p in profiles)))
    teams = sorted(list(set(p['team'] for p in profiles)))
    
    print(f"✓ Unique locations count: {len(locations)}")
    print(f"✓ Locations: {', '.join(locations)}")
    
    print(f"\n✓ Unique teams count: {len(teams)}")
    print(f"✓ Teams: {', '.join(teams)}")
    
    return locations, teams


def test_6_specific_skill_search():
    """Test Case 6: Find profiles with specific skills"""
    print("\n" + "=" * 70)
    print("TEST 6: Search for Specific Skills")
    print("=" * 70)
    
    profiles = load_profiles_from_json(DATA_PATH)
    
    # Search for Python experts
    python_experts = [p for p in profiles if 'Python' in p.get('skills', [])]
    print(f"✓ Python experts found: {len(python_experts)}")
    print(f"✓ Names: {', '.join(p['name'] for p in python_experts[:5])}...")
    
    # Search for RAG experts
    rag_experts = [p for p in profiles if 'RAG' in p.get('skills', [])]
    print(f"\n✓ RAG experts found: {len(rag_experts)}")
    print(f"✓ Names: {', '.join(p['name'] for p in rag_experts[:5])}...")
    
    # Search for Kubernetes experts
    k8s_experts = [p for p in profiles if 'Kubernetes' in p.get('skills', [])]
    print(f"\n✓ Kubernetes experts found: {len(k8s_experts)}")
    if k8s_experts:
        print(f"✓ Names: {', '.join(p['name'] for p in k8s_experts)}")
    
    return python_experts, rag_experts, k8s_experts


def test_7_project_search():
    """Test Case 7: Find people who worked on specific projects"""
    print("\n" + "=" * 70)
    print("TEST 7: Search by Project Name")
    print("=" * 70)
    
    profiles = load_profiles_from_json(DATA_PATH)
    
    # Search for "Expertise Finder (RAG)" project
    expertise_finder_team = []
    for p in profiles:
        for proj in p.get('projects', []):
            if 'Expertise Finder' in proj.get('name', ''):
                expertise_finder_team.append(p['name'])
                break
    
    print(f"✓ People who worked on 'Expertise Finder': {len(expertise_finder_team)}")
    print(f"✓ Names: {', '.join(expertise_finder_team[:10])}...")
    
    # Search for "Campaign Anomaly Detection" project
    campaign_team = []
    for p in profiles:
        for proj in p.get('projects', []):
            if 'Campaign Anomaly Detection' in proj.get('name', ''):
                campaign_team.append(p['name'])
                break
    
    print(f"\n✓ People who worked on 'Campaign Anomaly Detection': {len(campaign_team)}")
    print(f"✓ Names: {', '.join(campaign_team[:10])}...")
    
    return expertise_finder_team, campaign_team


def test_8_location_filter():
    """Test Case 8: Filter by location"""
    print("\n" + "=" * 70)
    print("TEST 8: Filter by Location")
    print("=" * 70)
    
    profiles = load_profiles_from_json(DATA_PATH)
    
    # Filter by Bangalore
    bangalore_profiles = [p for p in profiles if p['location'] == 'Bangalore']
    print(f"✓ Profiles in Bangalore: {len(bangalore_profiles)}")
    print(f"✓ Names: {', '.join(p['name'] for p in bangalore_profiles[:5])}...")
    
    # Filter by Chennai
    chennai_profiles = [p for p in profiles if p['location'] == 'Chennai']
    print(f"\n✓ Profiles in Chennai: {len(chennai_profiles)}")
    print(f"✓ Names: {', '.join(p['name'] for p in chennai_profiles[:5])}...")
    
    # Filter by Remote
    remote_profiles = [p for p in profiles if p['location'] == 'Remote']
    print(f"\n✓ Remote profiles: {len(remote_profiles)}")
    if remote_profiles:
        print(f"✓ Names: {', '.join(p['name'] for p in remote_profiles[:5])}...")
    
    return bangalore_profiles, chennai_profiles, remote_profiles


def test_9_team_filter():
    """Test Case 9: Filter by team"""
    print("\n" + "=" * 70)
    print("TEST 9: Filter by Team")
    print("=" * 70)
    
    profiles = load_profiles_from_json(DATA_PATH)
    
    # Filter by Platform team
    platform_team = [p for p in profiles if p['team'] == 'Platform']
    print(f"✓ Platform team members: {len(platform_team)}")
    print(f"✓ Names: {', '.join(p['name'] for p in platform_team[:5])}...")
    
    # Filter by ML team
    ml_team = [p for p in profiles if p['team'] == 'ML']
    print(f"\n✓ ML team members: {len(ml_team)}")
    print(f"✓ Names: {', '.join(p['name'] for p in ml_team[:5])}...")
    
    # Filter by Security team
    security_team = [p for p in profiles if p['team'] == 'Security']
    print(f"\n✓ Security team members: {len(security_team)}")
    if security_team:
        print(f"✓ Names: {', '.join(p['name'] for p in security_team)}")
    
    return platform_team, ml_team, security_team


def test_10_combined_filter():
    """Test Case 10: Combined filters (location + skill)"""
    print("\n" + "=" * 70)
    print("TEST 10: Combined Filters (Location + Skill)")
    print("=" * 70)
    
    profiles = load_profiles_from_json(DATA_PATH)
    
    # Find Python experts in Bangalore
    bangalore_python = [
        p for p in profiles 
        if p['location'] == 'Bangalore' and 'Python' in p.get('skills', [])
    ]
    print(f"✓ Python experts in Bangalore: {len(bangalore_python)}")
    if bangalore_python:
        print(f"✓ Names: {', '.join(p['name'] for p in bangalore_python)}")
    
    # Find RAG experts in Platform team
    platform_rag = [
        p for p in profiles 
        if p['team'] == 'Platform' and 'RAG' in p.get('skills', [])
    ]
    print(f"\n✓ RAG experts in Platform team: {len(platform_rag)}")
    if platform_rag:
        print(f"✓ Names: {', '.join(p['name'] for p in platform_rag)}")
    
    return bangalore_python, platform_rag


def test_11_experience_distribution():
    """Test Case 11: Analyze experience distribution"""
    print("\n" + "=" * 70)
    print("TEST 11: Experience Distribution")
    print("=" * 70)
    
    profiles = load_profiles_from_json(DATA_PATH)
    
    experiences = [p.get('experience_years', 0) for p in profiles]
    
    print(f"✓ Average experience: {sum(experiences) / len(experiences):.1f} years")
    print(f"✓ Minimum experience: {min(experiences)} years")
    print(f"✓ Maximum experience: {max(experiences)} years")
    
    # Junior (0-3 years)
    junior = [p for p in profiles if p.get('experience_years', 0) <= 3]
    print(f"\n✓ Junior (0-3 years): {len(junior)} people")
    
    # Mid-level (4-6 years)
    mid_level = [p for p in profiles if 4 <= p.get('experience_years', 0) <= 6]
    print(f"✓ Mid-level (4-6 years): {len(mid_level)} people")
    
    # Senior (7+ years)
    senior = [p for p in profiles if p.get('experience_years', 0) >= 7]
    print(f"✓ Senior (7+ years): {len(senior)} people")
    
    return junior, mid_level, senior


def test_12_specific_person_lookup():
    """Test Case 12: Look up specific person"""
    print("\n" + "=" * 70)
    print("TEST 12: Specific Person Lookup")
    print("=" * 70)
    
    profiles = load_profiles_from_json(DATA_PATH)
    
    # Look up Rohan Iyer
    rohan = [p for p in profiles if p['name'] == 'Rohan Iyer'][0]
    
    print(f"✓ Name: {rohan['name']}")
    print(f"✓ Title: {rohan['title']}")
    print(f"✓ Team: {rohan['team']}")
    print(f"✓ Location: {rohan['location']}")
    print(f"✓ Experience: {rohan['experience_years']} years")
    print(f"✓ Skills: {', '.join(rohan['skills'][:8])}...")
    print(f"✓ Number of projects: {len(rohan['projects'])}")
    
    return rohan


def run_all_tests():
    """Run all test cases"""
    print("\n")
    print("*" * 70)
    print("*" + " " * 68 + "*")
    print("*" + " " * 15 + "INTERNAL EXPERTISE FINDER TEST SUITE" + " " * 16 + "*")
    print("*" + " " * 68 + "*")
    print("*" * 70)
    print("\n")
    
    try:
        # Run all tests
        test_1_load_profiles()
        test_2_extract_project_info()
        test_3_create_document_content()
        test_4_convert_to_documents()
        test_5_unique_locations_and_teams()
        test_6_specific_skill_search()
        test_7_project_search()
        test_8_location_filter()
        test_9_team_filter()
        test_10_combined_filter()
        test_11_experience_distribution()
        test_12_specific_person_lookup()
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY")
        print("=" * 70)
        print("\nCompare the output above with 'test_expected_outputs.md'")
        print("to verify everything is working correctly.")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
