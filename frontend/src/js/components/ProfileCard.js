/**
 * Created by alexmelagrano on 5/11/18.
 */
import React from 'react';
import { NotificationManager } from 'react-notifications';
import EventsTable from './EventsTable';
import AppContext from '../app-context';

export default class ProfileCard extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            eventData: {},
            isLimited: false,
            upvote: true
        }
    }

    async componentWillMount() {
        const eventsQuery = this.props.context.state.eventsQuery(this.props.profile['id'])
        const eventsResp = await fetch('api/events/counts?' + eventsQuery, {credentials: "same-origin"});
        const events = await eventsResp.json();
        this.setState({eventData: events['counts'], isLimited: events['is_limited']})
    }
    
    async newDrinkEvent(eventTypeID) {
        // TODO : Making a loading animation
        // TODO : Return if profileType isn't drinker
        console.log('new drink event of type: ' + eventTypeID);
        const resp = await fetch('api/drinkers/' + this.props.profile['id'] + '/events/' + eventTypeID, {
            method: this.state.upvote ? 'POST' : 'DELETE',
            credentials: 'same-origin'
        });
        const success = await resp.json();
        const deleteOrSave = this.state.upvote ? 'save' : 'delete';
        if (success) {
            this.componentWillMount();
            NotificationManager.success('Successfully ' + deleteOrSave + 'd an event!');
        } else {
            NotificationManager.error('Failed to ' + deleteOrSave + ' an event. Go find JNorth if this is bad.');
        }
    }

    isUpvoteMode() {
        return this.state.upvote;
    }

    toggleVoteType(e) {
        e.stopPropagation();
        this.setState({upvote: !this.state.upvote});
    }

    render() {
        let tableClasses = "table mb-0";
        if (!this.props.profile["is_public"]) {
            tableClasses += 'mask-values';
        }

        const profilePhoto = this.props.profile["profile_photo"];
        const bio = this.props.profile["bio_line"];
        const name = this.props.profile["name"];
        const maxDaysDry = this.props.profile["max_days_dry"];
        const numDaysDry = this.props.profile["num_days_dry"];
        const profileColor = this.state.upvote ? "bg-green" : "bg-red";
        const crestIcon = this.props.profile["primary_group"]["profile_photo"]

        return (
            <div className="profile-card flipper">
                <div className="card-front shadow-lg bg-plus p-3">
                    <div className="rounded-corners p-1 bg-red">
                        <img src={ profilePhoto } alt="profile_photo_active"
                             className="border-med border-dark rounded-corners w-100"/>
                    </div>
                    <div className="bg-white border-med border-dark rounded-circle position-absolute card-icon">
                        <img src={ crestIcon } width="50px" alt="Chi_Sigma_Crest_Icon"/>
                    </div>
                    <div className="text-uppercase mt-4">
                        <h4 className="text-black-50 mb-1">Known As</h4>
                        <h2 className="text-red mb-0">{ name }</h2>
                    </div>
                </div>
                <div className="card-back shadow-lg bg-plus p-3">
                    <div className={ "rounded-circle position-absolute card-icon p-1 " + profileColor } onClick={ this.toggleVoteType.bind(this) }>
                        <img src={ profilePhoto } width="50px" alt="profile_photo_active"
                             className="border-med border-dark rounded-circle "/>
                    </div>
                    <div className="text-uppercase ml-1 mt-3">
                        <h6 className="text-black-50 mb-1">Max Days Dry: { maxDaysDry }</h6>
                        <h4 className="text-red mb-0">Dry Streak: { numDaysDry }</h4>
                    </div>
                    <div className="bg-white border border-dark rounded m-1 p-2">
                        <AppContext.Consumer>
                            {(context) => (
                                <EventsTable classes={ tableClasses } context={ context } isUpvoteMode={ this.isUpvoteMode.bind(this) } newDrinkEvent={ this.newDrinkEvent.bind(this) } eventTypes={ this.props.eventTypes } eventTimes={ this.props.eventTimes } events={ this.state.eventData }/>
                            )}
                         </ AppContext.Consumer>
                    </div>
                    <div className="p-2">
                        <span className="font-weight-bold">Details</span>
                        <i className="text-black-50 small d-block">This profile has hidden events: { this.state.isLimited.toString() }</i>
                    </div>
                </div>
            </div>
        )
    }
}
