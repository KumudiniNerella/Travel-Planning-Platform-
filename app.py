import streamlit as st
import os
import helper
import base64
import uuid
from datetime import datetime, date, timedelta
import matplotlib.pyplot as plt
from streamlit_login_auth_ui.widgets import __login__
import warnings
warnings.filterwarnings("ignore")

def set_bg_hack(main_bg):
    file_extension = os.path.splitext(main_bg)[-1].lower().replace(".", "")
    with open(main_bg, "rb") as f:
        image_data = f.read()
    base64_image = base64.b64encode(image_data).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url(data:image/{file_extension};base64,{base64_image});
            background-size: cover
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    __login__obj = __login__(auth_token = "dk_prod_XHG9DC6V4EMCB2J8X6GJA01AFJMS",
                    company_name = "Shims",
                    width = 200, height = 250,
                    logout_button_name = 'Logout', hide_menu_bool = False,
                    hide_footer_bool = False,
                    lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

    LOGGED_IN = __login__obj.build_login_ui()

    if LOGGED_IN == True:
        set_bg_hack('image.jpg')
        st.title("Travel booking system")
        fetched_cookies = __login__obj.cookies
        if '__streamlit_login_signup_ui_username__' in fetched_cookies.keys():
            username = fetched_cookies['__streamlit_login_signup_ui_username__']

        st.write(f"Welcome, {username}!")
        user_data = helper.get_userdata_by_username(username)
        if not helper.get_user_document(username):
            helper.update_user_data(user_data, update = False)
        saved_user_data = helper.get_user_document(username)

        st.sidebar.subheader("Menu")
        user_choice = st.sidebar.selectbox(label = "select",
                                           options = ["update details",
                                                      "recommendations",
                                                      "search destination by name",
                                                      "search destination by preference",
                                                      "view bookings",
                                                      "book a trip",
                                                      "plots"])
        if user_choice == "update details":
            country_states_dict = helper.get_country_state_mapping()
            all_activities_list = helper.get_all_destination_activities()
            saved_user_data['gender'] = st.selectbox(label = "gender", options = ["male", "female"])
            saved_user_data['country'] = st.selectbox(label = "country", options = list(country_states_dict.keys()))
            saved_user_data['state'] = st.selectbox(label = "state", options = country_states_dict[saved_user_data['country']])
            saved_user_data['bestSeason'] = st.selectbox(label = "season", options = ['Winter','Monsoon','Summer'])
            saved_user_data['activityTags'] = st.multiselect(label = "activityType", options = all_activities_list)
            saved_user_data['travelBudget'] = st.number_input(label = "budget", min_value=100, max_value=None, value="min", step=1)
            if st.button("save data"):
                helper.update_user_data(saved_user_data, update = True)
                st.success("Data saved successfully!")
        elif user_choice == "recommendations":
            saved_user_data = helper.get_user_document(username)
            if not (saved_user_data['activityTags']):
                st.warning("Please update your details/preferences!")
            else:
                rec_choice = st.selectbox(label = "select", options = ['state','bestSeason','activityTags'])
                rec_data = helper.recommend_destination(username, var = rec_choice)
                for attraction in rec_data:
                    with st.expander(attraction["name"]):
                        # st.image(attraction["imagePath"], caption=attraction["oneLineDescription"])
                        st.write(f"**Description:** {attraction['oneLineDescription']}")
                        st.write(f"**Tags:** {', '.join(attraction['activityTags'])}")
                        st.write(f"**Average Cost:** ₹{attraction['averageCost']}")
                        st.write(f"**Best Season:** {attraction['bestSeason']}")
                        st.write(f"**Country:** {attraction['country']}")
                        st.write(f"**State:** {attraction['state']}")
                        st.write(f"**Rating:** {attraction['rating']}")
                        attr = ", ".join(attraction["popularAttractions"])
                        st.write(f"**Popular Nearby Attractions:** {attr}")
        elif user_choice == "search destination by name":
            search_name = st.text_input(label = "name")
            if search_name:
                matching_destinations = helper.search_destination_by_name(search_name)
                if not matching_destinations:
                    st.write("No matching destinations found!")
                else:
                    st.write("Matching destinations:")
                    selected_destination = st.selectbox(label = "destination", options = [destination['name'] for destination in matching_destinations])
                    attraction = [i for i in matching_destinations if i['name'] == selected_destination][0]
                    with st.expander(attraction["name"]):
                        # st.image(attraction["imagePath"], caption=attraction["oneLineDescription"])
                        st.write(f"**Description:** {attraction['oneLineDescription']}")
                        st.write(f"**Tags:** {', '.join(attraction['activityTags'])}")
                        st.write(f"**Average Cost:** ₹{attraction['averageCost']}")
                        st.write(f"**Best Season:** {attraction['bestSeason']}")
                        st.write(f"**Country:** {attraction['country']}")
                        st.write(f"**State:** {attraction['state']}")
                        st.write(f"**Rating:** {attraction['rating']}")
                        attr = ", ".join(attraction["popularAttractions"])
                        st.write(f"**Popular Nearby Attractions:** {attr}")

                    if st.button("Add to cart"):
                        cart_destination = [i for i in matching_destinations if i['name'] == selected_destination][0]
                        if 'cart' in saved_user_data:
                            saved_user_data['cart'].append(cart_destination['destinationid'])
                        else:
                            saved_user_data['cart'] = [cart_destination['destinationid']]
                        print("saving the data", saved_user_data['cart'])
                        helper.update_user_data(saved_user_data, update = True)
                        st.success("Added destination to cart")
        elif user_choice == "search destination by preference":
            country_states_dict = helper.get_country_state_mapping()
            all_activities_list = helper.get_all_destination_activities()
            saved_user_data = helper.get_user_document(username)
            search_country = st.selectbox(label = "country", options = list(country_states_dict.keys()))
            search_state = st.selectbox(label = "state", options = country_states_dict[search_country])
            search_season = st.selectbox(label = "season", options = ['Winter','Monsoon','Summer'])
            search_activity = st.multiselect(label = "activityType", options = all_activities_list)
            matching_destinations = helper.search_destination(search_state, search_season, search_activity)
            if not matching_destinations:
                st.write("No matching destinations found!")
            else:
                st.write("Matching destinations:")
                selected_destination = st.selectbox(label = "destination", options = [destination['name'] for destination in matching_destinations])
                attraction = [i for i in matching_destinations if i['name'] == selected_destination][0]
                with st.expander(attraction["name"]):
                    # st.image(attraction["imagePath"], caption=attraction["oneLineDescription"])
                    st.write(f"**Description:** {attraction['oneLineDescription']}")
                    st.write(f"**Tags:** {', '.join(attraction['activityTags'])}")
                    st.write(f"**Average Cost:** ₹{attraction['averageCost']}")
                    st.write(f"**Best Season:** {attraction['bestSeason']}")
                    st.write(f"**Country:** {attraction['country']}")
                    st.write(f"**State:** {attraction['state']}")
                    st.write(f"**Rating:** {attraction['rating']}")
                    attr = ", ".join(attraction["popularAttractions"])
                    st.write(f"**Popular Nearby Attractions:** {attr}")

                if st.button("Add to cart"):
                    cart_destination = [i for i in matching_destinations if i['name'] == selected_destination][0]
                    if 'cart' in saved_user_data:
                        saved_user_data['cart'].append(cart_destination['destinationid'])
                    else:
                        saved_user_data['cart'] = cart_destination['destinationid']
                    helper.update_user_data(saved_user_data, update = True)
                    st.success("Added destination to cart")
        elif user_choice == "view bookings":
            saved_user_data = helper.get_user_document(username)
            all_booking_list = helper.get_all_bookings_of_user(saved_user_data["username"])
            if not all_booking_list:
                st.warning("No booking found")
            else:
                booking_id = st.selectbox(label = "booking id", options = [bid['bookingid'] for bid in all_booking_list])
                booking_details = [i for i in all_booking_list if i['bookingid'] == booking_id][0]
                del booking_details['destinationid']
                #st.write(booking_details)
                attraction = booking_details
                with st.expander(attraction["bookingid"]):
                    # st.image(attraction["imagePath"], caption=attraction["oneLineDescription"])
                    st.write(f"**username:** {attraction['username']}")
                    st.write(f"**destinationname:** {attraction['destinationname']}")
                    st.write(f"**noOfDays:** ₹{attraction['noOfDays']}")
                    st.write(f"**noOfPeople:** {attraction['noOfPeople']}")
                    st.write(f"**bookingDatetime:** {attraction['bookingDatetime']}")
                    st.write(f"**startDate:** {attraction['startDate']}")
                    st.write(f"**EndDate:** {attraction['EndDate']}")
                    st.write(f"**totalCost:** {attraction['totalCost']}")
                if st.button("delete"):
                    if (datetime.strptime(booking_details['startDate'], "%d/%m/%Y").date() - timedelta(days=2)) > date.today():
                        helper.delete_booking(booking_id)
                        st.success(f"Booking {booking_details['bookingid']} deleted successfully!")
                    else:
                        st.error("Can only delete bookings with greated than 2 days from start date!")
        elif user_choice == "book a trip":
            saved_user_data = helper.get_user_document(username)
            if ('cart' in saved_user_data) and (saved_user_data['cart']):
                all_destination_cart_list = helper.get_all_destination(saved_user_data['cart'])
                selected_destination = st.selectbox(label = "destination", options = [destination['name'] for destination in all_destination_cart_list])
                min_start_date = datetime.today() + timedelta(days=5)
                start_date = st.date_input("Select start date", min_start_date, min_value=min_start_date)
                min_end_date = start_date + timedelta(days=2)
                end_date = st.date_input("Select end date", min_end_date, min_value=min_end_date)
                noofpeople = st.number_input("Number of people",min_value = 1,step=1)
                cost_dict = {}
                cost_dict['cost for each person per day'] = [i for i in all_destination_cart_list if i['name'] == selected_destination][0]['averageCost']
                cost_dict[f'cost for each person for {(end_date - start_date).days} days'] = int(cost_dict['cost for each person per day']) * (end_date - start_date).days
                cost_dict['Total Cost'] = int(cost_dict[f'cost for each person for {(end_date - start_date).days} days']) * noofpeople
                attraction = [i for i in all_destination_cart_list if i['name'] == selected_destination][0]
                with st.expander(attraction["name"]):
                    # st.image(attraction["imagePath"], caption=attraction["oneLineDescription"])
                    st.write(f"**Description:** {attraction['oneLineDescription']}")
                    st.write(f"**Tags:** {', '.join(attraction['activityTags'])}")
                    st.write(f"**Average Cost:** ₹{attraction['averageCost']}")
                    st.write(f"**Best Season:** {attraction['bestSeason']}")
                    st.write(f"**Country:** {attraction['country']}")
                    st.write(f"**State:** {attraction['state']}")
                    st.write(f"**Rating:** {attraction['rating']}")
                    attr = ", ".join(attraction["popularAttractions"])
                    st.write(f"**Popular Nearby Attractions:** {attr}")
                    st.write(f"**cost for each person per day:** {cost_dict['cost for each person per day']}")
                    st.write(f"**cost for each person for {(end_date - start_date).days} days:** {cost_dict[f'cost for each person for {(end_date - start_date).days} days']}")
                    st.write(f"**Total Cost:** {cost_dict['Total Cost']}")

                if st.button("confirm booking"):
                    booked_destination = [i for i in all_destination_cart_list if i['name'] == selected_destination][0]
                    d = {}
                    d['username'] = saved_user_data['username']
                    d['bookingid'] = uuid.uuid4().hex
                    d['destinationid'] = booked_destination['destinationid']
                    d['destinationname'] = booked_destination['name']
                    d['noOfDays'] = (end_date - start_date).days
                    d['noOfPeople'] = noofpeople
                    d['bookingDatetime'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                    d['startDate'] = start_date.strftime('%d/%m/%Y')
                    d['EndDate'] = end_date.strftime('%d/%m/%Y')
                    d['totalCost'] = cost_dict['Total Cost']
                    helper.insert_booking(d)
                    st.success(f"Booking confirmed successfully with id {d['bookingid']}!")
            else:
                st.warning("No destination added to cart!")
        else:
            all_states = helper.get_state_visit_mapping()
            selected_states = st.multiselect("Select multiple States", all_states, default=['Maharashtra'])
            if st.button("plot"):
                filtered_state_population = {state:val for state,val in all_states.items() if state in selected_states}
                if filtered_state_population:
                    st.subheader("State vs no of visits")
                    fig, ax = plt.subplots()
                    ax.bar(filtered_state_population.keys(), filtered_state_population.values(), color='coral')
                    ax.set_xlabel('State')
                    ax.set_ylabel('no of visits')
                    ax.set_title('State vs no of visits')
                    st.pyplot(fig)

if __name__ == "__main__":
    main()
    # recommendations show dropdown based on country, season, activity and use expander to show details
    # add background image of travel
