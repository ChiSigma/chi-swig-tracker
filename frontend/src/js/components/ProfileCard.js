/**
 * Created by alexmelagrano on 5/11/18.
 */
import React from 'react';
import { NotificationManager } from 'react-notifications';
import { geolocated } from 'react-geolocated';
import EventsTable from './EventsTable';
import AppContext from '../app-context';

class ProfileCard extends React.Component {
    constructor(props) {
        super(props);

        this.appState = () => { return this.props.context.state };
        this.auth = () => { return this.props.context.auth };
        this.state = {
            eventData: {},
            isLimited: false,
            upvote: true,
            editable: false
        }
    }

    async componentWillMount() {
        const eventsQuery = this.appState().eventsQuery(this.props.profile['id'])
        const events = await fetch('api/events/counts?' + eventsQuery, {credentials: "same-origin"});
        const editable = await this.auth().isEditable(this.props.profile);
        this.setState({eventData: events['counts'], isLimited: events['is_limited'], editable})
    }

    async fetchLocation() {

    }

    async newDrinkEvent(eventTypeID) {
        const location = { location: 'unknown' }
        if (this.props.isGeolocationAvailable && this.props.isGeolocationEnabled) {
            const latitude = this.props.coords.latitude;
            const longitude = this.props.coords.longitude;
            location.location = latitude + ',' + longitude
        }

        const response = await fetch('api/drinkers/' + this.props.profile['id'] + '/events/' + eventTypeID, {
            method: this.state.upvote ? 'POST' : 'DELETE',
            credentials: 'same-origin',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify(location)
        });
        const deleteOrSave = this.state.upvote ? 'save' : 'delete';
        if (!response.error) {
            this.componentWillMount();
            NotificationManager.success('Successfully ' + deleteOrSave + 'd an event!');
        }
    }

    isUpvoteMode() {
        return this.state.upvote;
    }

    isEditable() {
        return this.state.editable;
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
        const name = this.props.profile["name"];
        const maxDaysDry = this.props.profile["max_days_dry"];
        const numDaysDry = this.props.profile["num_days_dry"];
        const profileColor = this.state.upvote ? "bg-green" : "bg-red";
        const crestIcon = this.props.profile["primary_group"] ? this.props.profile["primary_group"]["profile_photo"] : profilePhoto

        return (
            <div className="profile-card flipper">
                <div className="card-front shadow-lg bg-plus p-3">
                    <div className="rounded-corners p-1 bg-red">
                        <div className="profile-photo-container border-med border-dark rounded-corners border-dark">
                            <img src={ profilePhoto } alt="profile_photo_active" className="profile-photo"/>
                        </div>
                    </div>
                    <div className="bg-white border-med border-dark rounded-circle position-absolute card-icon-container">
                        <img src={ crestIcon } className="card-icon" alt="Chi_Sigma_Crest_Icon"/>
                    </div>
                    <div className="text-uppercase mt-4">
                        <h4 className="text-black-50 mb-1">Known As</h4>
                        <h2 className="text-red mb-0">{ name }</h2>
                    </div>
                </div>
                <div className="card-back shadow-lg bg-plus p-3">
                    <div className={ "rounded-circle position-absolute card-icon-container p-1 " + profileColor } onClick={ this.toggleVoteType.bind(this) }>
                        <img src={ profilePhoto } alt="profile_photo_active"
                             className="border-med border-dark rounded-circle card-icon "/>
                    </div>
                    <div className="text-uppercase ml-1 mt-3">
                        <h6 className="text-black-50 mb-1">Max Days Dry: { maxDaysDry }</h6>
                        <h4 className="text-red mb-0">Dry Streak: { numDaysDry }</h4>
                    </div>
                    <div className="bg-white border border-dark rounded m-1 p-2">
                        <AppContext.Consumer>
                            {(context) => (
                                <EventsTable
                                    classes={ tableClasses }
                                    profileType={ this.appState().profileType }
                                    isEditable={ this.isEditable.bind(this) }
                                    isUpvoteMode={ this.isUpvoteMode.bind(this) }
                                    newDrinkEvent={ this.newDrinkEvent.bind(this) }
                                    eventTypes={ this.props.eventTypes }
                                    eventTimes={ this.props.eventTimes }
                                    events={ this.state.eventData }/>
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

export default geolocated({
    watchPosition: true,
})(ProfileCard)
