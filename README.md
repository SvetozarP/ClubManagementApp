Creating an Archery club management app with Django.

Web App Concept: "Archery Club Manager with Field Booking"
Description: This web app will help club administrators and members manage events, track training sessions, and book archery fields. It will streamline the club’s daily operations by organizing event schedules, member profiles, training progress, and field availability.

It comprises of 12 models, powered by PostgreSQL, managing:
- The Club Mission statement
- The Club History
- Testimonials, received by participants in beginner's courses, Have-A-Go sessions and other club activities
- Club News
- Club Events
- Club Announcements
- Club calendar, displaying field bookings for individual archers and club events (with RESTful get endpoint at api/combined-bookings/), allowing the functionality to register participation in events through the calendar itself
- Field configuration
- Booking of shooting sessions
- Creation and management of events and registering / unregistering participation
- Creation and management of club news
- Recording of details for each shooting session
- Receiving messages, accessible to the admin users from non-registered users
- Secure registration / profile completion and profile management logic, based on tokens
- Ability for the user to update his password and recover lost passwords - verified by site administrators on a token-based system

Web pages:

1. Landing page

![image](https://github.com/user-attachments/assets/47e8bf4f-bc93-4d67-b8c2-bdcd51089d7c)

  
2. Login page with links for forgotten password - allowing the user to request a token and received token page for password reset

![image](https://github.com/user-attachments/assets/7ddea4d3-df8a-4a60-aa1f-b189b58536c6)

   
3. Club History page

![image](https://github.com/user-attachments/assets/c544d33b-ba3f-4402-816e-aca907836e4c)

  
4. Membership information page

![image](https://github.com/user-attachments/assets/d1781f1a-55a4-4cb5-aeda-84beaec946d8)

5. News page giving summary of the website's active news and the ability of the user to read more where he needs to. Admin users can amend news through the details view. The page also supports view of past news, which are not so relevant at present (arhchived).

![image](https://github.com/user-attachments/assets/e3dcffec-50e2-4f64-bacd-1669b0249a97)

6. Events page, giving summary of upcomming events and providing users with ability to see more details for each event, register participation and admins to edit / alter events. The page supports access to past events too, so users have information on what have they missed.

![image](https://github.com/user-attachments/assets/881b5ebd-9288-4749-8492-61743817c666)

7. Asynchronious Contact us page providing method for communication to the general public with the admins of the website, which does not slow down an user who wants to reach out.

![image](https://github.com/user-attachments/assets/cbf8d10f-e31d-4989-a263-af3907c27e02)

Modified user login logic, where user can login using his email or his username.

Logged in users receive access to:
1. Log out button, which instantly logs the user out
2. User profile page, where they can see, based on their access level:
   1. For normal registered users:
      - Ability to edit their profile, being able to change their Phone number, Address, profile image and password
      - Book a shooting session
      - Record details for a shooting session
      - See summary for booked sessions in the near future (allowing them to buddy up with other archers on the field)
      - See past club announcements
    2. Admin users gain all this access plus:
       - Ability to see all registered users and provide help amending other details (email, username, first name, last name) for the registered users, also ability to request and provide the user with reset password token
       - Ability to create club announcements
       - Ability to create news
       - Ability to create events
       - Ability to create new users, who then can register using token for their registration
      
  ![image](https://github.com/user-attachments/assets/1ca9ce96-5968-4367-9cf9-268eaac73ffc)


 3. JavaScript powered club calendar page (RESTful) which displays details for any booked shooting sesions and also upcoming club events

  ![image](https://github.com/user-attachments/assets/459d9188-0c5e-462e-b9bd-1081e07c3b91)


The profile page itself, gives the ability of the user to see his profile details, see any outstanding club announcements (that he hasn't read yet), see upcoming events, for which he has registered participation, see any 
upcoming shooting sessions, that the user has booked, see his latest training notes (last 10).
Admin users can see also any incoming requests from non-members and also any requests for password reset (with the ability to provide the token to the user, requesting password reset).

Users are forced to choose secure passwords which have to contain:
- At least 10 characters
- At least 1 uppercase letter
- At least 1 digit
- At least 1 special character
- Password must not be similar to the user's username
- Password must not be based on dictionary word

To enhance user's protection, the site also limits the failed login requests to 5 per 15 minutes. There are further limits to requesting reset tokens (1 per hour) and limits to sending contact requests to the club.
  
The site's superuser benefits from the use of a Django Unfold powered admin panel, through which, he has full access to all of the site's data and ability to modify all of the dynamic content described above. Models registered in the admin site benefit from search ability, filtering and convenient list displays.

![image](https://github.com/user-attachments/assets/aef8fe26-1b6d-4211-bd1f-ac6d0d716fd2)


Majority of the views, giving access to the site's resources are class-based. The site is equipped with over 16 forms, which help users achieve various requests and actions, necessary for their experience.

The app also contains 2 main templates (base website and profile base website) which are extended by further over custom built DTL templates, some with JavaScript functionality. Styling is achieved through 14 separate cascading style sheets,
describing the schemas for the different templates.

For enhanced functionality and data security, the site also utilises SimpleDjangoHistory, monitoring changes in the Mission statament, Club history, Field configuration and Membership Info models.

Future developments and extensions:
- Ability to manage scores, provide users with feedback on their performance and dashboards, based on the scores that they have achieved.
- Classification / handicap management
- User awards and distribution
- Various reports, based on performance, active members, field usability, members activity
- Email integration
- Field management and limits for each distance
- Booking limits and restrictions
- Integration with other software like IANSEO for tournament and result management and like Golden Records to help with score management
- Integration with user's calendars
- Ability to integrate with mobile application
