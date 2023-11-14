import ispyb_lib
import nsls2api_lib
import argparse
import sys

#input
# proposal
# visit number

def main(args=[]):
    parser = argparse.ArgumentParser(
        description="Create people, visit, and proposal information in ISPyB. Check whether these already exist."
    )
    parser.add_argument(
        "--proposal",
        type=int,
        help="The names of the proposal.",
    )
    parser.add_argument(
        "--visit",
        type=str,
        help="Name of the visit."
    )
    parser.add_argument(
        "--beamline",
        type=str,
        help="Beamline name."
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        help="Show more log messages. (Use -vv for even more.)",
    )

    args = parser.parse_args(args or sys.argv[1:])
    if args.verbose:
        if args.verbose == 1:
            logging.basicConfig(level="INFO")
        if args.verbose == 2:
            logging.basicConfig(level="DEBUG")
        else:
            logging.basicConfig()  # "WARNING" by default

    proposal = args.proposal
    visit = args.visit
    beamline = args.beamline

    if not proposal or not visit or not beamline:
        raise RuntimeError("please define proposal, visit, AND beamline")

    # get people
    # create people, if necessary
    # create proposal
    # create visit
    ispyb_lib.add_users_for_proposal(proposal, visit, beamline)

if __name__ == "__main__":
    main()
