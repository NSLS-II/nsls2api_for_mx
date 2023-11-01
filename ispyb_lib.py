import nsls2api
import ispyb.factory

conn = ispyb.open("/etc/ispyb/ispybConfig.cfg")
cnx = conn.conn
cursor = cnx.cursor()
core = ispyb.factory.create_data_area(ispyb.factory.DataAreaType.CORE, conn)

def queryDB(q):
  cursor.execute(q)
  try:
    return list(cursor.fetchall())
  except TypeError:
    return 0

def queryOneFromDB(q):
  cursor.execute(q)
  try:
    return list(cursor.fetchone())[0]
  except TypeError:
    return 0

# get list numbers from a queryDB() call
# be able to handle input from a query result or raw list
def get_unique_ids(id_list):
    id_set = set()
    for _id in id_list:
        if type(_id) == tuple:
            id_set.add(_id[0])
        elif type(_id) == int:
            id_set.add(_id)
    return list(id_set)

# works for query results
def get_in_string(ids):
    if len(ids)> 1:
        multi_id_string = ""
        for _id in get_unique_ids(ids):
            id_string = str(_id)
            multi_id_string += f"'{id_string}', "
        return multi_id_string[:-2]  # get rid of trailing comma
    else:
        return f"'{str(ids[0])}'"

def get_ispyb_proposal_ids():
    '''
    Get all proposals in the ISPyB database by starting from
    BLSessions
    '''
    # go through all of Session_has_person and get all BLSessions
    query = "SELECT sessionId FROM Session_has_Person;"
    session_ids = queryDB(query)
    session_id_string = ""
    if len(session_ids)> 1:
        for session_id in get_unique_ids(session_ids):
            session_str = str(session_id)
            session_id_string += f"'{session_str}', "
        session_id_string = session_id_string[:-2]
    else:
        session_id_string = f"'{str(session_ids[0])}'"
    # get proposals
    query = f"SELECT proposalId from BLSession where sessionId in ({session_id_string});"
    proposal_ids = queryDB(query)
    return get_unique_ids(proposal_ids)

def get_proposal_numbers(proposal_ids):
    query = f"SELECT proposalNumber from Proposal where proposalId in ({get_in_string(proposal_ids)});"
    proposal_nums = queryDB(query)
    return get_unique_ids(proposal_nums)

def remove_all_usernames_for_proposal(proposal_id, dry_run=True):
    if dry_run:
        print(f"Clearing usernames for proposal {proposal_id}")
        return
    persons_on_proposal = core.retrieve_persons_for_proposal("mx", proposal_id)
    query = f"SELECT proposalId from Proposal where proposalNumber={proposal_id}"
    proposal_ids = queryDB(query)
    query = f"SELECT sessionId FROM BLSession where proposalId={proposal_id}"  # note difference of what we call proposal_id vs BLSession's name, which is proposal_number
    session_ids = queryDB(query)
    people_in_sessions = set()
    for session_id in session_ids:
        query = "SELECT personId FROM Session_has_Person WHERE sessionId={session_id}"
        people_in_session = queryDB(query)
        people_in_sessions.add(people_in_session)
    if dry_run:
        print(f"Dry run: remove usernames for proposal: {people_in_sessions}")
    # clear all Session_has_Person for the proposal
    for session_id in session_ids:
        query = "DELETE Session_has_Person where session_id={session_id}"
        delete_session_has_person = queryDB(query)
        print(delete_session_has_person)

def add_usernames_for_proposal(proposal_id, current_usernames, dry_run=True):
    if type(current_usernames) != set:
        raise ValueError("current usernames must be a set")
    usernames_to_add = current_usernames
    if dry_run:
        print(f"users to add: {usernames_to_add}")
        return
    query = "DELETE proposal_has_person where username={username}"
    for person in usernames_to_add:
        session_id = get_session_id()  # TODO where do we get this?
        person_id=get_person_id(person) # personIdFromProposal()
        params = core.get_session_has_person()
        params['session_id'] = session_id
        params['person_id'] = person_id
        #params['role']  #define? can we identify from nsls2api? perhaps going into the user info?
        params['remove'] = True
        response = core.upsert_session_has_person(params)
        print(f"session add_person: {response}")

def set_usernames_for_proposal(proposal_id):
    ...

def reset_users_for_proposal(proposal_id, dry_run=True):
    ''' given a proposal id, take all of the users off an existing set of visits
        in ispyb and add the current users in '''
    # first, clear all existing usernames for the proposal_id in ISPyB
    # alternative, get usernames here, then remove/add as necessary at the bottom
    remove_all_usernames_for_proposal(proposal_id)
    # next, get the users who should be on the current proposal
    current_usernames = nsls2api.get_from_api(f"proposal/{proposal_id}/usernames")
    # finally, set all visits of the proposal to these users
    # alternative, modify the tables as necessary given the previous and current user lists
    # TODO consider what should happen if old proposals have no users
    add_usernames_for_proposal(proposal_id, set(current_usernames['usernames']), dry_run=True)


def proposalIdFromProposal(propNum):
  q = ("select proposalId from Proposal where proposalNumber = " + str(propNum))
  return (queryOneFromDB(q))


def maxVisitNumfromProposal(propNum):
  propID = proposalIdFromProposal(propNum)
  q = ("select max(visit_number) from BLSession where proposalId = " + str(propID))
  return (queryOneFromDB(q))

def setup_proposal(proposal, users):
    # if doesn't exist, make it
    #   highest visit number is 1
    # find highest visit number
    # create newest proposal (highest number)
    # add users to proposal
    # add users to session
    pass
