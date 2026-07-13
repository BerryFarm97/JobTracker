from datetime import date
import time
from database import initialize_database, add_application, get_active_applications, update_status, archived_status, get_archived, change_archive_status, return_filtered_apps, get_search_results


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
        "View Archived Applications",
        "Filter Applications By Status",
        "Search for applications",
        "Exit"
    ]
    for num, option in enumerate(menu_options, start=1):
        print(f"{num}. {option}")
    try:
        choice = int(input("What would you like to do?: "))
        if 0 < choice <= len(menu_options):
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
        "application_date": str(date.today()),
        "notes": notes,
        "status": status,
        "archived": 0
    }

    return application


def view_applications():
    sort_choice = get_sorting_choice()
    stored_apps = get_active_applications(sort_choice)
    if not stored_apps:
        print("Nothing to view yet.")
        return
    
    for app in stored_apps:
        print("----------------------------")
        print(f"Company: {app['company_name'].title()}")
        print(f"  Job Title: {app['job_title'].title()}")
        print(f"  Salary Range: {app['salary_range']}")
        print(f"  Location: {app['location'].title()}")
        print(f"  Date Applied: {app['application_date'].title()}")
        print(f"  Status: {app['status'].title()}")
        print(f"  Notes: {app['notes'].title()}")
        print("----------------------------")


def update_application_status():
    update_options = [
        "Applied",
        "Interviewing",
        "Offer",
        "Rejected",
        "Ghosted",
        "Withdrawn"
    ]
    sort_choice = get_sorting_choice()
    stored_apps = get_active_applications(sort_choice)

    while True:
        try:
           
            if not stored_apps:
                print("Nothing to update yet.")
                return
            else:
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
                update_status(selected_app["id"], selected_status)
                print(f"Successfully updated {selected_app['company_name']} application status")
                break
            else:
                print("Not a valid option. Please try again.")
                continue
        except ValueError:
            print("Not a valid option. Please try again.")
            continue


def archive_application():
    sort_choice = get_sorting_choice()
    stored_apps = get_active_applications(sort_choice)
    if not stored_apps:
            print("Nothing to archive yet.")
            return
    while True:
        try:
            for num, app in enumerate(stored_apps, start=1):
                    print(f"{num}. {app['company_name']} - {app['job_title']} - {app['status']}")
            choice = int(input("Which application would you like to archive?: "))
            if 0 < choice <= len(stored_apps):
                app_to_archive = stored_apps[choice - 1]
                archived_status(app_to_archive["id"])
                print(f"Success! {app_to_archive['company_name']} has been archived")
                break
            else:
                print("Not a valid option. Please try again")
        except ValueError:
            print("Not a valid option. Please try again.")
            continue


def view_archived_apps():
    sort_choice = get_sorting_choice()
    archived_apps = get_archived(sort_choice)
    if not archived_apps:
        print("Nothing to view yet.")
        return

    for num, app in enumerate(archived_apps, start=1):
        print(f"{num}. {app['company_name']} | {app['job_title']} | {app['status']}\n")
    while True:
        choice = input("Would you like to re-add a archived application?(y/n): ").strip().lower()
        try:
            if choice in ('y', 'yes'):
                chose_app = int(input("Which app do you want to change?: "))
                if 0 < chose_app <= len(archived_apps):
                    app_to_restore = archived_apps[chose_app - 1]
                    change_archive_status(app_to_restore['id'])
                    print(f"Successfully restored your {app_to_restore['company_name']} application!")
                    return
                else:
                    print("Invalid option. Please try again")

            elif choice in ('n', 'no'):
                return
            else:
                print("Invalid option. Please try again.")
                continue
        except ValueError:
            print("Invalid option. Please try again.")
            continue
        

def view_filtered_apps():
    status_options = [
        "Applied",
        "Interviewing",
        "Offer",
        "Rejected",
        "Ghosted",
        "Withdrawn"
    ]
    for num, status in enumerate(status_options, start=1):
        print(f"{num}. {status}")
    while True:
        try:
            choice = int(input("What application status are you looking for?: "))
            if 0 < choice <= len(status_options):
                status_choice = status_options[choice - 1]
                sort_choice = get_sorting_choice()
                filtered_list = return_filtered_apps(status_choice, sort_choice)

                if not filtered_list:
                    print(f"No active applications with the status: {status_choice}")
                    return
                for num, app in enumerate(filtered_list, start=1):
                    print(f"{num}. {app['company_name']} | {app['job_title']} | {app['salary_range']} | {app['application_date']} | {app['notes']} | {app['status']}")
                return
            else:
                print("Invalid option. Please try again.")
                
        except ValueError:
            print("Invalid option. Please try again.")


def search_for_applications():
    searching = True
    while searching:
        phrase = input("Please enter a keyword or phrase to search: ").strip().lower()
        if not phrase:
            print("Please enter at least one character.")
            continue
        
        sort_choice = get_sorting_choice()
        results = get_search_results(phrase, sort_choice)
        if not results:
            print("No applications matched that search")
            
        
        for num, result in enumerate(results, start=1):
            print(
                f"{num}. Company name: {result['company_name'].title()} | "
                f"Job Title: {result['job_title'].title()} | Salary Range: {result['salary_range']} | "
                f"Application Date: {result['application_date']} | Notes: {result['notes']} | "
                f"Application Status: {result['status'].title()}"
            )
        
        while True:
            search_again = input("Would you like to make another search?(y/n): ").strip().lower()
            if search_again in ('y', 'yes'):
                break

            elif search_again in ('n', 'no'):
                searching = False
                break

            else:
                print("Invalid option. Please try again.")
                continue  


def get_sorting_choice():
    sorting_options = [
        'Newest',
        'Oldest',
        'Company Name',
        'Application Status'
    ]
    while True:
        for num, option in enumerate(sorting_options, start=1):
            print(f"{num}. {option}")
        try:
            sort_choice = int(input("How would you like to sort them?: "))
            if 0 < sort_choice <= len(sorting_options):
                selected_choice = sorting_options[sort_choice - 1]
                return selected_choice
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Invalid option. Please try again.")


def edit_application():
    editable_options = [
        'Company Name',
        'Job Title',
        'Salary Range',
        'Location',
        'Notes'
    ]
    
    while True:
        try:
            sort_choice = get_sorting_choice()
            stored_apps = get_active_applications(sort_choice)
            if not stored_apps:
                print("Nothing to update yet.")
                return
            #print all apps and asking user which one they want to edit.
            #then after getting the app to edit ask the user what they want to change on THAT application
            #Ask the user for the new value of that choice
            #return that new value to SQL and update the table with the new value
            #print a success statment
            #Ask the user if they would like to edit another part of that same app
            #if yes then ask then again what they want to change etc...
            #if no ask the user if they want to edit another app
            #if yes re-start the whole function
            #if no return to the main menu
        except ValueError:
            print("Invalid option. Please try again.")


def main():
    initialize_database()

    while True:
        
        selection = get_menu_choice()
        if not selection:
            continue

        elif selection == 1:
            new_application = create_application()
            add_application(new_application)
        
        elif selection == 2:
                view_applications()

        elif selection == 3:
            update_application_status()

        elif selection == 4:
                archive_application()
        
        elif selection == 5:
            view_archived_apps()

        elif selection == 6:
            view_filtered_apps()
        
        elif selection == 7:
            search_for_applications()

        elif selection == 8:
            break




if __name__ == "__main__":
    main()