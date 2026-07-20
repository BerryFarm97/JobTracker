from datetime import date
from urllib.parse import urlsplit
from csv_exporter import convert_db_csv
from pathlib import Path
from database import (
    initialize_database,
    add_application,
    get_active_applications,
    update_status,
    archived_status,
    get_archived,
    change_archive_status,
    return_filtered_apps,
    get_search_results,
    edit_application_values,
    delete_archived_app,
    get_csv_data,
)

# This project should keep track of jobs I have applied to.
# Company name, date applied, if a response was given (interview, offer, declined, ignored, or if I retract my application)
# any notes ive made, salary range, job title etc.

# This app should allow the user to enter a job applied to
# User should be able to view all applications
# User should be able to remove/archive applications
# User should be able to update application info
# User should be able to exit the program at any time by typing "exit" or pressing a specific number
# (
# When adding a job the user should be prompted to enter the company name, job title, salary range, and on-site or work from home.
# The program should then grab the current date and time (based on the users timezone) and store that with the Add application
# )
ALLOWABLE_SCHEMES = (
    "http",
    "https",
)


def url_validation_handler(url):

    try:
        url_split = urlsplit(url)

        scheme = url_split.scheme
        hostname = url_split.hostname
    except ValueError:
        return False, "\nURL parse failed. Please re-check the URL and try again."

    if scheme not in ALLOWABLE_SCHEMES:
        return False, "\nPlease enter a URL with HTTP or HTTPS"

    if not hostname:
        return False, "\nURL hostname cannot be empty. Check the URL and try again."

    return True, ""


def yes_no_handler(question):
    while True:
        formatted_response = input(question).strip().lower()

        if formatted_response in ("y", "yes"):
            return True

        elif formatted_response in ("n", "no"):
            return False

        else:
            print("\nNot a valid entry. Please enter y or n.")


def get_optional_url():
    question = "\nWould you like to enter a URL?(y/n): "
    response_result = yes_no_handler(question)

    if not response_result:
        return None

    while True:
        url = input("\nPlease enter the url, or leave blank to cancel: ")
        url_clean = url.strip()

        if not url_clean:
            return None

        validation_result = url_validation_handler(url_clean)

        is_valid, error_message = validation_result

        if is_valid:
            return url_clean
        if not is_valid:
            print(error_message)


def get_required_text(prompt):
    while True:
        user_input = input(prompt).strip()

        if not user_input:
            print("\nThis field cannot be blank")

        else:
            return user_input


def get_optional_text(prompt):
    user_input = input(prompt).strip()
    return user_input


def get_menu_choice():
    menu_options = [
        "Add a job",
        "View Applications",
        "Update Application",
        "Archive Application",
        "View Archived Applications",
        "Filter Applications By Status",
        "Search for applications",
        "Convert Table to CSV",
        "Exit",
    ]

    while True:
        for num, option in enumerate(menu_options, start=1):
            print(f"{num}. {option}")

        try:
            choice = int(input("What would you like to do?: "))
            if 0 < choice <= len(menu_options):
                return choice
            elif choice < 0:
                print(
                    f"\nNegative numbers are not accepted, please enter a number between 1 and {len(menu_options)}."
                )
                continue
            else:
                print(
                    f"\nInvalid option, please enter a number between 1 and {len(menu_options)}."
                )
                continue
        except ValueError:
            print(
                f"\nInvalid option, please only enter whole numbers between 1 and {len(menu_options)}."
            )
            continue


def create_application():

    company_name_prompt = "Company name: "
    job_title_prompt = "Job Title: "
    salary_range_prompt = "Salary Range (optional): "
    location_prompt = "Job Location (optional): "
    notes_prompt = "Any notes? (optional): "
    status = "Applied"

    company_name = get_required_text(company_name_prompt)
    job_title = get_required_text(job_title_prompt)
    salary_range = get_optional_text(salary_range_prompt)
    location = get_optional_text(location_prompt)
    notes = get_optional_text(notes_prompt)
    url = get_optional_url()

    application = {
        "company_name": company_name,
        "job_title": job_title,
        "salary_range": salary_range,
        "location": location,
        "application_date": str(date.today()),
        "notes": notes,
        "status": status,
        "url": url,
        "archived": 0,
    }

    application_added = add_application(application)

    if not application_added:
        print(
            f"\nDatabase was unable to add the {application['job_title']} application at {application['company_name']}. Please try again later.\n"
        )
        return

    elif application_added:
        print(
            f"\nSuccessfully created {application['job_title']} application at {application['company_name']}.\n"
        )


def view_applications():
    sort_choice = get_sorting_choice()
    stored_apps = get_active_applications(sort_choice)

    if stored_apps is None:
        print(
            "Unable to load applications because of database error. Please try again."
        )
        return

    elif not stored_apps:
        print("\nNothing to view yet.")
        return

    for app in stored_apps:
        print("----------------------------")
        print(f"  Company: {app['company_name']}")
        print(f"  Job Title: {app['job_title']}")
        print(f"  Salary Range: {app['salary_range']}")
        print(f"  Location: {app['location']}")
        print(f"  Date Applied: {app['application_date']}")
        print(f"  Status: {app['status']}")
        print(f"  Notes: {app['notes']}")
        print(f"  Url: {app['url']}")
        print("----------------------------")


def update_applications():
    changeable_params = ["Application Details", "Application Status"]
    while True:
        for num, param in enumerate(changeable_params, start=1):
            print(f"{num}. {param}")
        try:
            choice = int(input("\nWhich would you like to update?: "))

            if 0 < choice <= len(changeable_params):
                if choice == 1:
                    edit_application()
                    break
                elif choice == 2:
                    update_application_status()
                    break
            else:
                print("\nPlease enter a number. Try again.")
                continue
        except ValueError:
            print("\nPlease only enter numbers. Try again.")
            continue


def update_application_status():
    update_options = [
        "Applied",
        "Interviewing",
        "Offer",
        "Rejected",
        "Ghosted",
        "Withdrawn",
    ]
    sort_choice = get_sorting_choice()
    stored_apps = get_active_applications(sort_choice)

    if stored_apps is None:
        print(
            "Unable to load applications because of a database error. Please try again.\n"
        )
        return

    elif not stored_apps:
        print("\nNothing to update yet.\n")
        return

    while True:
        try:

            if not stored_apps:
                print("\nNothing to update yet.\n")
                return
            else:
                for num, app in enumerate(stored_apps, start=1):
                    print(
                        f"{num} {app['company_name']} - {app['job_title']} - {app['status']}"
                    )
                app_to_update = int(
                    input("\nWhich application status would you like to update?: ")
                )
                if 0 < app_to_update <= len(stored_apps):
                    selected_app = stored_apps[app_to_update - 1]
                    break
                else:
                    print("\nNot a valid option. Please try again.")
                    continue
        except ValueError:
            print("\nNot a valid option. Please try again.")
            continue
    while True:
        try:
            for pos, option in enumerate(update_options, start=1):
                print(f"{pos}. {option}")
            new_status = int(input("What is the new status?: "))
            if 0 < new_status <= len(update_options):
                selected_status = update_options[new_status - 1]
                if (
                    selected_status == selected_app["status"]
                ):  # Check for if user selected status is same as current and re-prompt user to enter a new status
                    print(
                        f"\nThat application already has {selected_status} as its current status. Please select a different status.\n"
                    )
                    continue
                status_updated = update_status(selected_app["id"], selected_status)
                if not status_updated:
                    print(
                        f"\nDatabase failed to apply status change: {selected_status} to application: {selected_app['company_name']} | {selected_app['job_title']}.\n"
                    )
                    return
                else:
                    print(
                        f"\nSuccessfully updated {selected_app['company_name']} | {selected_app['job_title']} application status to {selected_status}\n"
                    )
                break
            else:
                print("\nNot a valid option. Please try again.\n")
                continue
        except ValueError:
            print("\nNot a valid option. Please try again.\n")
            continue


def edit_application():
    editing = True

    editable_options = {
        "Company Name": "company_name",
        "Job Title": "job_title",
        "Salary Range": "salary_range",
        "Location": "location",
        "Notes": "notes",
        "Url": "url",
    }

    editable_keys = list(editable_options.keys())
    while editing:
        sort_choice = get_sorting_choice()
        stored_apps = get_active_applications(sort_choice)

        if stored_apps is None:
            print(
                "Unable to load applications because of a database error. Please try again."
            )
            return

        elif not stored_apps:
            print("\nNothing to update yet.")
            return

        for num, app in enumerate(stored_apps, start=1):
            print(
                f"{num}. Company name: {app['company_name']} | "
                f"Job Title: {app['job_title']} | Salary Range: {app['salary_range']} | "
                f"Application Date: {app['application_date']} | "
                f"Application Status: {app['status'].title()}"
            )
        while True:
            try:
                app_edit = int(input("\nWhich app would you like to edit?: "))

                if 0 < app_edit <= len(stored_apps):
                    app_selected = stored_apps[app_edit - 1]
                    break
                else:
                    print("\nInvalid option. Please try again.")
            except ValueError:
                print("\nInvalid option. Please try again.")

        app_to_edit = edit_helper(editable_keys, editable_options, app_selected)
        if not app_to_edit:
            return False

        while True:
            edit_another = (
                input("\nWould you like to edit another application?(y/n): ")
                .strip()
                .lower()
            )

            if edit_another in ("y", "yes"):
                break
            elif edit_another in ("n", "no"):
                print("\nReturning to main menu.\n")
                editing = False
                break
            else:
                print("\nPlease enter y or n.")


def get_required_edit_text(prompt):
    while True:
        user_input = input(prompt).strip()

        if not user_input:
            print("This field cannot be blank")

        elif user_input.lower() == ":cancel":
            return False, None

        else:
            return True, user_input


def get_optional_edit_text(prompt):
    user_input = input(prompt).strip()

    if not user_input:
        return True, ""

    elif user_input.lower() == ":cancel":
        return False, None

    else:
        return True, user_input


def get_url_edit_text(prompt):
    while True:
        user_input = input(prompt).strip()

        if not user_input:
            return True, ""

        elif user_input.lower() == ":cancel":
            return False, None
        is_valid, error_message = url_validation_handler(user_input)

        if not is_valid:
            print(error_message)
            continue
        return True, user_input


def edit_helper(editable_keys, editable_options, app_selected):
    while True:
        for num, editable_key in enumerate(editable_keys, start=1):
            print(f"{num}. {editable_key}")
        try:
            user_choice = int(input("\nWhat would you like to change?: "))

            if 0 < user_choice <= len(editable_keys):
                selected_key = editable_keys[user_choice - 1]
                selected_column = editable_options[selected_key]
            else:
                print("\nInvalid option. Please try again.")
                continue
        except ValueError:
            print("\nPlease enter a number.")
            continue

        prompt = (
            f"Enter the new {selected_key}, or type :cancel to keep the current value: "
        )
        if selected_column in ("company_name", "job_title"):
            is_valid, user_response = get_required_edit_text(prompt)

        elif selected_column in ("salary_range", "location", "notes"):
            is_valid, user_response = get_optional_edit_text(prompt)

        elif selected_column == "url":
            is_valid, user_response = get_url_edit_text(prompt)

        if not is_valid:
            return False

        updated_database = edit_application_values(
            app_selected["id"], selected_column, user_response
        )

        if not updated_database:
            print(
                "\nDatabase unable to update application information. Please try again later.\n"
            )
            return False
        elif updated_database:
            if user_response == "":
                print(
                    f"{selected_key} was successfully cleared for application {app_selected['company_name']} | {app_selected['job_title']}."
                )
            else:
                print(
                    f"\n{selected_key} was successfully changed to {user_response} for application {app_selected['company_name']} | {app_selected['job_title']}."
                )

        while True:
            edit_same = (
                input(
                    "\nWould you like to make another change on this application?(y/n): "
                )
                .strip()
                .lower()
            )

            if edit_same in ("y", "yes"):
                break
            elif edit_same in ("n", "no"):
                return True
            else:
                print("\nPlease enter y or n.")


def archive_application():
    sort_choice = get_sorting_choice()
    stored_apps = get_active_applications(sort_choice)
    if stored_apps is None:
        print(
            "Unable to load applications because of a database error. Please try again."
        )
        return

    elif not stored_apps:
        print("\nNothing to archive yet.")
        return

    while True:
        try:
            for num, app in enumerate(stored_apps, start=1):
                print(
                    f"{num}. {app['company_name']} - {app['job_title']} - {app['status']}"
                )
            choice = int(input("\nWhich application would you like to archive?: "))
            if 0 < choice <= len(stored_apps):
                app_to_archive = stored_apps[choice - 1]
                app_archived = archived_status(app_to_archive["id"])
                if not app_archived:
                    print(
                        f"Database unable to archive: {app_to_archive['company_name']} | {app_to_archive['job_title']}. Please try again."
                    )
                    break

                elif app_archived:
                    print(
                        f"\nSuccessfully archived {app_to_archive['company_name']} | {app_to_archive['job_title']}."
                    )
                    break
            else:
                print("\nNot a valid option. Please try again")
        except ValueError:
            print("\nNot a valid option. Please try again.")
            continue


def view_archived_apps():
    sort_choice = get_sorting_choice()
    user_choices = ["Restore", "Permanently Delete", "Exit"]

    while True:
        try:
            archived_apps = get_archived(sort_choice)

            if archived_apps is None:
                print(
                    "Unable to load applications because of a database error. Please try again."
                )
                return False

            elif not archived_apps:
                print("\nNo archived applications.")
                return False

            for num, app in enumerate(archived_apps, start=1):
                print(
                    f"{num}. {app['company_name']} | {app['job_title']} | {app['status']}"
                )

            print("----------------------------------------")

            for num, choice in enumerate(user_choices, start=1):
                print(f"{num}. {choice}")

            user_choice = int(input("What would you like to do?: "))

            if user_choice == 1:
                while True:
                    refreshed_apps = get_archived(sort_choice)

                    if refreshed_apps is None:
                        print(
                            "Unable to load applications because of a database error. Please try again."
                        )
                        return False

                    elif not refreshed_apps:
                        print("\nNo more archived applications.")
                        return False

                    restore = restore_archived_helper(refreshed_apps, sort_choice)

                    if not restore:
                        return
                    while True:
                        restore_again_choice = (
                            input(
                                "\nWould you like to restore another application?(y/n): "
                            )
                            .strip()
                            .lower()
                        )
                        if restore_again_choice in ("y", "yes"):
                            break

                        elif restore_again_choice in ("n", "no"):
                            print("\nReturning to the main menu.\n")
                            return

                        else:
                            print("\nInvalid option. Please try again.")

            elif user_choice == 2:
                while True:
                    refreshed_apps = get_archived(sort_choice)
                    if refreshed_apps is None:
                        print(
                            "Unable to load applications because of a database error. Please try again."
                        )
                        return False

                    elif not refreshed_apps:
                        print("\nNo archived applications.")
                        return False

                    delete = delete_archived_helper(refreshed_apps, sort_choice)

                    if not delete:
                        return
                    while True:
                        delete_again_choice = (
                            input(
                                "\nWould you like to delete another application?(y/n): "
                            )
                            .strip()
                            .lower()
                        )

                        if delete_again_choice in ("y", "yes"):
                            break

                        elif delete_again_choice in ("n", "no"):
                            print("\nReturning to the main menu.\n")
                            return

                        else:
                            print("\nInvalid option. Please try again.")

            elif user_choice == 3:
                print("\nReturning to the main menu.\n")
                return

            else:
                print("\nInvalid option. Please try again.")
                continue
        except ValueError:
            print("\nPlease enter a valid number.")


def delete_archived_helper(archived_apps, sort_choice):
    while True:
        try:
            if not archived_apps:
                print("\nNo applications left to delete.")

                print("\nReturning to choice menu.\n")
                return False

            for num, app in enumerate(archived_apps, start=1):
                print(
                    f"{num}. {app['company_name']} | {app['job_title']} | {app['status']}\n"
                )

            user_choice = int(
                input("\nWhich app would you like to permanently remove?: ")
            )

        except ValueError:
            print("\nInvalid option. Please try again.")
            continue

        if 0 < user_choice <= len(archived_apps):
            selected_application = archived_apps[user_choice - 1]
            while True:
                user_confirm = (
                    input(
                        f"\nAre you sure you want to permanently delete {selected_application['company_name']} | {selected_application['job_title']}?(y/n): "
                    )
                    .strip()
                    .lower()
                )

                if user_confirm in ("y", "yes"):
                    perm_deleted = delete_archived_app(selected_application["id"])
                    if not perm_deleted:
                        print(
                            f"\nDatabase was unable to delete {selected_application['company_name']} | {selected_application['job_title']}. Please try again later."
                        )
                        break

                    print(
                        f"\nPermanently deleted {selected_application['company_name']} | {selected_application['job_title']}."
                    )
                    has_apps = get_archived(sort_choice)
                    if has_apps is None:
                        print(
                            "Unable to load applications because of a database error. Please try again."
                        )
                        return False

                    elif not has_apps:
                        print("\nNo more archived applications.")
                        return False

                    else:
                        return True

                elif user_confirm in ("n", "no"):
                    return False

                else:
                    print("Invalid option. Please enter y or n.")
                    continue

        else:
            print("\nInvalid selection. Please try again.")
            continue


def restore_archived_helper(archived_apps, sort_choice):
    while True:
        if not archived_apps:
            print("\nThere are no archived applications.")
            print("\nReturning to main menu.\n")
            return False

        for num, app in enumerate(archived_apps, start=1):
            print(
                f"{num}. {app['company_name']} | {app['job_title']} | {app['status']}\n"
            )

        try:
            chose_app = int(input("\nWhich application would you like to restore?: "))

            if 0 < chose_app <= len(archived_apps):
                app_to_restore = archived_apps[chose_app - 1]
                application_restored = change_archive_status(app_to_restore["id"])
                if not application_restored:
                    print(
                        f"Database unable to restore: {app_to_restore['company_name']} | {app_to_restore['job_title']}. Please try again."
                    )
                    return False

                elif application_restored:
                    print(
                        f"\nSuccessfully restored your {app_to_restore['company_name']} | {app_to_restore['job_title']} application!"
                    )
                has_apps = get_archived(sort_choice)
                if has_apps is None:
                    print(
                        "Unable to load applications because of a database error. Please try again."
                    )
                    return False

                elif not has_apps:
                    print("\nNo more archived applications.")
                    return False

                else:
                    return True

            else:
                print("\nInvalid option. Please try again")
                continue

        except ValueError:
            print("\nInvalid option. Please try again.")
            continue


def view_filtered_apps():
    status_options = [
        "Applied",
        "Interviewing",
        "Offer",
        "Rejected",
        "Ghosted",
        "Withdrawn",
    ]

    for num, status in enumerate(status_options, start=1):
        print(f"{num}. {status}")
    while True:
        try:
            choice = int(input("\nWhat application status are you looking for?: "))
            if 0 < choice <= len(status_options):
                status_choice = status_options[choice - 1]
                sort_choice = get_sorting_choice()
                filtered_list = return_filtered_apps(status_choice, sort_choice)

                if filtered_list is None:
                    print(
                        "Unable to load applications because of a database error. Please try again."
                    )
                    return

                elif not filtered_list:
                    print(f"\nNo active applications with the status: {status_choice}")
                    return

                for num, app in enumerate(filtered_list, start=1):
                    print(
                        f"{num}. {app['company_name']} | {app['job_title']} | {app['salary_range']} | {app['application_date']} | {app['notes']} | {app['status']}"
                    )
                return
            else:
                print("\nInvalid option. Please try again.")

        except ValueError:
            print("\nInvalid option. Please try again.")


def search_for_applications():
    searching = True
    while searching:
        phrase = input("\nPlease enter a keyword or phrase to search: ").strip().lower()
        if not phrase:
            print("\nPlease enter at least one character.")
            continue

        sort_choice = get_sorting_choice()
        results = get_search_results(phrase, sort_choice)

        if results == None:
            print("\nDatabase unable to complete search request. Please try again.\n")
            return

        elif not results:
            print("\nNo applications matched that search.\n")

        else:
            for num, result in enumerate(results, start=1):
                print(
                    f"{num}. Company name: {result['company_name'].title()} | "
                    f"Job Title: {result['job_title'].title()} | Salary Range: {result['salary_range']} | "
                    f"Application Date: {result['application_date']} | Notes: {result['notes']} | "
                    f"Application Status: {result['status'].title()}"
                )

        while True:
            search_again = (
                input("\nWould you like to make another search?(y/n): ").strip().lower()
            )
            if search_again in ("y", "yes"):
                break

            elif search_again in ("n", "no"):
                searching = False
                break

            else:
                print("\nInvalid option. Please try again.")
                continue


def get_sorting_choice():
    sorting_options = ["Newest", "Oldest", "Company Name", "Application Status"]
    while True:
        for num, option in enumerate(sorting_options, start=1):
            print(f"{num}. {option}")
        try:
            sort_choice = int(input("\nHow would you like to sort them?: "))
            if 0 < sort_choice <= len(sorting_options):
                selected_choice = sorting_options[sort_choice - 1]
                return selected_choice
            else:
                print("\nInvalid option. Please try again.")
        except ValueError:
            print("\nInvalid option. Please try again.")


def csv_conversion():
    sub_menu_options = {
        "Active applications only": "active",
        "Archived applications only": "archived",
        "All applications": "all",
    }

    for num, key in enumerate(sub_menu_options, start=1):
        print(f"{num}. {key}")

    while True:
        try:
            user_choice = int(input("What applications would you like to convert?: "))
            if 0 < user_choice <= len(sub_menu_options):
                selected_key = list(sub_menu_options.keys())[user_choice - 1]
                sub_menu_selection = sub_menu_options[selected_key]
                break
            else:
                print("Invalid options please enter a number between 1 and 3.")
        except ValueError:
            print("Please only enter a number between 1 and 3.")

    csv_data = get_csv_data(sub_menu_selection)

    if csv_data is None:
        print("Unable to retrieve application data for export. Please try again later.")
        return

    if csv_data == []:
        print("\nThere are no applications to export.\n")
        return

    final_path = get_export_path()

    csv_dictionaries = [dict(row) for row in csv_data]
    converted = convert_db_csv(csv_dictionaries, final_path)

    if not converted:
        print("\nUnable to export data. Please try again later.\n")

    else:
        print(f"\nCSV file successfully saved at {final_path}.\n")


def get_export_path():
    filename = Path("applications_table.csv")

    folder = input(
        "\nWhere should the file be saved? If left empty CSV will be saved in project folder: "
    ).strip()

    if folder == "":
        folder = Path(__file__).resolve().parent

    folder_formatted = Path(folder)

    candidate_path = folder_formatted / filename

    counter = 1

    while candidate_path.exists():
        new_name = f"{filename.stem}({counter}){filename.suffix}"
        candidate_path = folder_formatted / new_name

        if not candidate_path.exists():
            break

        else:
            counter += 1

    return candidate_path


def main():
    db_start = initialize_database()

    if not db_start:
        print("\nDatabase failed to initialize. Please try again.\n")
        return

    while True:

        selection = get_menu_choice()
        if not selection:
            continue

        elif selection == 1:
            create_application()

        elif selection == 2:
            view_applications()

        elif selection == 3:
            update_applications()

        elif selection == 4:
            archive_application()

        elif selection == 5:
            view_archived_apps()

        elif selection == 6:
            view_filtered_apps()

        elif selection == 7:
            search_for_applications()

        elif selection == 8:
            csv_conversion()

        elif selection == 9:
            break


if __name__ == "__main__":
    main()
