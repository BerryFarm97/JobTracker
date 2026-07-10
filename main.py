from datetime import date
import time


#This project should keep track of jobs I have applied to.
#Company name, date applied, if a response was given (interview, offer, declined, ignored, or if I retract my application)
#any notes ive made, salary range, job title etc.

#This app should allow the user to enter a job applied to
#User should be able to view all applications
#User should be able to remove/archive applications
#User should be able to update application info
#User should be able to exit the program at any time by typing "exit" or pressing a specific number
#(
#When adding a job the user should be prompted to enter the company name, job title, salary range, and on-site or work from home.
#The program should then grab the current date and time (based on the users timezone) and store that with the Add application
#)

def get_menu_choice():
    menu_options = [
        "Add a job",
        "View Applications",
        "Update Application",
        "Archive Application",
        "Exit"
    ]
    for num, option in enumerate(menu_options, start=1):
        print(f"{num}. {option}")
    try:
        choice = int(input("What would you like to do?: "))
        if 0 < choice < 6:
            return choice
        else:
            print("Invalid entry. Please try again")
    except ValueError:
        print("Invalid selection. Please try again.")
        time.sleep(.5)
        return None

def create_application():
    company_name = input("Company name: ")
    job_title = input("Job Title: ")
    salary_range = input("Salary Range: ")
    location = input("Job Location(onsite,work from home, hybrid): ")
    notes = input("Any notes?: ")
    status = "Applied"

    application = {
        "company_name": company_name,
        "job_title": job_title,
        "salary_range": salary_range,
        "location": location,
        "date": str(date.today()),
        "notes": notes,
        "status": status
    }

    return application

def view_applications(stored_apps):
    for app in stored_apps:
        print("----------------------------")
        print(f"Company: {app['company_name'].title()}")
        print(f"  Job Title: {app['job_title'].title()}")
        print(f"  Salary Range: {app['salary_range']}")
        print(f"  Location: {app['location'].title()}")
        print(f"  Date Applied: {app['date'].title()}")
        print(f"  Status: {app['status'].title()}")
        print(f"  Notes: {app['notes'].title()}")
        print("----------------------------")
        time.sleep(1)

def update_application_status(stored_apps):
    update_options = [
        "Applied",
        "Interviewing",
        "Offer",
        "Rejected",
        "Ghosted",
        "Withdrawn"
    ]
    while True:
        try:
            for num, app in enumerate(stored_apps, start=1):
                print(f"{num} {app['company_name']} - {app['job_title']} - {app['status']}")
            app_to_update = int(input("Which application status would you like to update?: "))
            if 0 < app_to_update <= len(stored_apps):
                selected_app = stored_apps[app_to_update - 1]
                break
            else:
                print("Not a valid option. Please try again.")
                continue
        except ValueError:
            print("Not a valid option. Please try again.")
            continue
    while True:
        try:
            for pos, option in enumerate(update_options, start=1):
                print(f"{pos}. {option}")
            new_status = int(input("What is the new status?: "))
            if 0 < new_status <= len(update_options):
                selected_status = update_options[new_status - 1]
                selected_app["status"] = selected_status
                print(f"Successfully updated {selected_app['company_name']} application status")
                break
            else:
                print("Not a valid option. Please try again.")
                continue
        except ValueError:
            print("Not a valid option. Please try again.")
            continue



def main():
    stored_applications = []
    while True:

        selection = get_menu_choice()
        if not selection:
            continue
        elif selection == 1:
            new_application = create_application()
            stored_applications.append(new_application)

        elif selection == 2:
            if not stored_applications:
                print("Nothing to view yet")
                time.sleep(.5)
                continue
            else:
                view_applications(stored_applications)
        elif selection == 3:
            if not stored_applications:
                print("Nothing to update yet.")
                time.sleep(.5)
                continue
            else:
                update_application_status(stored_applications)

        elif selection == 5:
            break

        else:
            break






if __name__ == "__main__":
    main()
