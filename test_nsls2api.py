import httpx
import time

base_url = "https://api-staging.nsls2.bnl.gov"

def get_from_api(url):
    if url:
        response = httpx.get(f"{base_url}/{url}")
        time.sleep(0.5)
        if response.status_code == httpx.codes.OK:
            return response.json()
        raise RuntimeError(f"failed to get value from {url}. response code: {response.status_code}")
    else:
        raise ValueError("url cannot be empty")
proposals_api = get_from_api("proposals/2022-3")
proposals = proposals_api[0]['proposals']
for proposal in proposals:
    pass #print(f"proposal: {proposal}")
datasessions_api = get_from_api("data_session/jaishima")
pass# print(datasessions_api.json())

facilities_api = get_from_api("facilities")
for facility in facilities_api:
    print(f"facility: {facility['name']}")
    #facility_info = get_from_api(f"facility/{facility['id']}")
    #print(facility_info)
    #facility_cycles = get_from_api(f"facility/{facility['id']}/cycles")
    #for cycle in facility_cycles:
    #    print(cycle['name'])
    print()
    #print("failure of facilities")

instruments = get_from_api("instruments")
for instrument in instruments:
    pass
    #print(f"instrument: {instrument}")
get_from_api(f"facility/{facility['id']}/cycles/proposals")
get_from_api(f"facility/{facility['id']}/cycles")
get_from_api(f"facility/{facility['id']}")
proposal = get_from_api(f"proposal/312064")  # FMX commissioning proposal
proposal_id = proposal['proposal_id']
print(f"proposalID: {proposal_id}")
cycle="2023-3"
print(f'proposals for cycle {cycle}: {get_from_api(f"proposals/{cycle}")}')
print(f'users for proposal {proposal_id}: {get_from_api(f"proposal/{proposal_id}/usernames")}')
get_from_api(f"proposal/{proposal_id}/users")  # full info on users
print(f'directories: {get_from_api(f"proposal/{proposal_id}/directories")}')
print(f'full info on proposal: {get_from_api(f"proposal/{proposal_id}")}')
get_from_api(f"proposal/{proposal_id}/group-membership")
