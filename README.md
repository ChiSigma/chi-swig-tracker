chi-swig-tracker
=================
We're some pretty competitive people here @ Chi Sigma. In our final year at Northeastern, we wanted to have a year
long challenge tracking various events amongst our members. But then we decided, why stop there? Why not include 
everyone? [So that's what we did.](https://swig.chisigma.co)

Some key items:
* Sorting is normalized. It is the Drinker/Group event count divided by the minimum of the total seconds from (now - selected sort window) or the (now - `created_at`), and then divided by the n of Drinkers/Groups. This allows Groups and Drinkers joining mid-way through our year long sprint to be fairly sorted.
* The total days that we've had this app running is shown in the header.
* You can hide event counts from public view, but when you are sorted, you will be sorted on your true event count.
* x event in a day is the count of events in the past 12 hours. It used to be set to 24, but it made things a bit
confusing. 
* Every night a midnight, if you (or every primary drinker in a group) hasn't had a drink in the past 24hrs, the
Dry Count will be updated.

Table of contents
=================

<!--ts-->
   * [chi-swig-tracker](#chi-swig-tracker)
   * [Table of contents](#table-of-contents)
   * [Sign Up](#sign-up)
      * [Drinker](#drinker)
      * [Groups](#groups)
      * [Group Types](#group-types)
   * [Event Actions](#event-actions)
      * [Add](#add)
      * [Delete](#delete)
   * [Filtering](#filtering)
      * [Filter Drinkers](#filter-drinkers)
      * [Filter Groups](#filter-groups)
   * [Preferences](#preferences)
      * [Name](#name)
      * [Profile Photos](#profile-photos)
      * [Privacy](#privacy)
      * [Membership Policies](#membership-policies) 
   * [Security & Bugs](#security-and-bugs)
   * [Dashboard Mode](#dashboard-mode)
<!--te-->

Sign Up
=================
Drinker
-----
To join as a new drinker - 'tis easy peasy lemon squeezy. Simply click the Login/Sign-up button, and a new drinker will automatically be created. All you need is a Google account which will be your login.

Groups
-----
To create a new group, you need to submit a request by sending a message to [here](https://www.facebook.com/chisigma).
Once the group is created, you'll be made an admin and will have full control over users and customizing preferences.

Group Types
-----
There are two types of group memberships: primary and ephemeral. You can only have a single primary membership and as many ephemeral memberships as you want. Group event counts are calculated by summing the event counts of all primary members - ephemeral ones are not included.

Ephemeral memberships allow you to be shown when someone filters to a specific group, but your events only benefit your primary group's count.

Event Actions
=================
You can add/delete events for any drinker who is a member of a group that you're in. Addition/Deletion is all honor system authenticated
so be a good person and drink responsibly. [Video How To](http://recordit.co/VtLRT6COA1)

Add
-----------------
To add an event, make sure the outline around your drinker profile is green and then click the event icon for the desired type.

Delete
-----------------
To delete an event, make sure the outline around your drinker profile is red and then click the event icon for the desired type.
You can only delete events that were created within a 30 minute window.

Filtering
=================
[Video How To](http://recordit.co/NyPGkhPpSo)

Filter Drinkers
-----------------
To view drinker profiles on the dashboard, select Drinkers from the dropdown in the Open Filter Dialog. You can then filter drinkers by the groups that they are in and/or down to a specific selection of drinkers.

Filter Groups
-----------------
To view group profiles on the dashboard, select Groups from the dropdown in the Open Filter Dialog. You can then filter groups by name.

Preferences
=================
Name
-----------------
Names are limited to 10 (or so) characters so nicknames work best.

Profile Photos
-----------------
Must be valid link(s) to photos that are accessible via the open webs.

For drinkers, a comma separated list of profile photos is supported (kinda?). Every 3 drinks, the next profile photo will be used (to show a progression of how you look at different numbers). This isn't required - one or none is sufficient.

For groups, only a single profile photo is supported.

Bio Line
-----------------
Limited to 26 characters (I think?). A short and sweet snippet of whatever you want to say.

Privacy
-----------------
These settings apply to both Drinkers and Groups. You will be shown notifications in the filter menu and on profile cards if certain things are being hidden due to privacy settings.
[Hidden Profiles](https://drive.google.com/file/d/1U0XtfOZ5S5QEzOrs_RaPMxpB9_uLjCTR/view?usp=sharing) & 
[Hidden Events](https://drive.google.com/file/d/10H-uxekA7Gue_26BA2sS6Q6gOirCg0h4/view?usp=sharing)

Members of your group will override these settings and will always be able to see you and your counts. These settings only apply to those outside your group.

There are three privacy types: public, hide events, and unlisted. 

Public means that anyone can see you on the dashboard, and they can see
your events table. 

Hide events will show you on the dasboard, but will remove your events from sums on the group dashboard and will hide them from showing in your events table. 

Unlisted means you will not show on the dashboard and all events will be hidden.

Membership Policies
-----------------
For Drinkers, this setting sets what kinds of groups that admins can add you to. For Groups, it sets whether or not drinkers can join your group.

The memberhsip policy types: public, primary, ephemeral, and private.

Public is that anyone can add you to a group as a primary or ephemeral member (they can only add you as a primary member if you don't already have one.)
A Public group is one that anyone can join as any type.

Primary will only allow you to be added to a group as a primary member and drinkers can only join a group as a primary member.

Ephemeral is the same as Primary, but joining/added as an ephemeral member.

Private is no one can add you to a group and drinkers cannot join your group without being added by an admin.

Security and Bugs
=================
If you find a security vulnerability or a serious bug, please let us know - we'll happily buy you a beer for it.

Dashboard Mode
=================
Filter to your desired drinkers/groups, select the desired sort type, and the click the Chi Sigma name in the bottom left corner (so it turns green).
The sorting of the dashboard will auto-update every 30 seconds.


                                        Idea                                          |     Difficulty (1-5)
|                                    -----------                                      |          :----:
| Dynamic profile pictures that update based on events                                | :white_check_mark:
| Disable +1/-1 buttons if not logged in                                              | :white_check_mark:
| Add live-ish data to staging                                                        | :white_check_mark:
| Add a footer                                                                        | :white_check_mark:
| Loading animations                                                                  | :white_check_mark:
| Success/Failure notifications                                                       | :white_check_mark:
| Finish Total Days component                                                         | :white_check_mark:
| Deploy this live                                                                    | :white_check_mark:
| Allow for other people to join in the counting                                      | :white_check_mark:
| Update the README with more deets                                                   | :white_check_mark:
| Custom back button action                                                           | 2
| Fetch memberships on toggle                                                         | 1
| Auto complete memberhsip forms                                                      | 1
| Check if profile photo links are valid on save                                      | 1
| Allow impersonation of users for superusers                                         | 2
| Add CI to this                                                                      | 3
