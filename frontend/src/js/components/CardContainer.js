/**
 * Created by alexmelagrano on 5/11/18.
 */
import React from 'react';

import MiniProfileCard from './MiniProfileCard';
import ProfileCard from './ProfileCard';

export default class SortWidget extends React.Component {
    constructor() {
        super();

        // TODO :: make request to drinkers to get the ID list
        this.state = {
            activeProfile: 0, // main, active profile ID
            profiles: [0, 0, 0, 0],
            show: false
        }; // main
        
        this.profileID = 1;

        this.handleShow = this.handleShow.bind(this);
        this.handleClose = this.handleClose.bind(this);
    }

    handleClose() {
        this.setState({ show: false });
    }

    handleShow() {
        this.setState({ show: true });
    }

    changeActiveProfile(activeProfile) {
        console.log('changing active profile!');
        this.setState({ activeProfile })
    }
    
    render() {
        const miniProfiles = this.state.profiles.map((profileID) =>
            <div className="m-4">
                <MiniProfileCard changeActiveProfile={ this.changeActiveProfile.bind(this) } profileID={ this.profileID } />
            </div>
        );
        return (
            <div className="container pt-4">
                <div className="modal">
                    <div className="bg-gray-transparent modal-backdrop h-100 d-flex justify-content-center align-items-center">
                        <div className="flip-container">
                            <ProfileCard />
                        </div>
                    </div>
                </div>
                <div className="row">
                    <div className="d-flex align-items-baseline justify-content-center flex-wrap">
                            { miniProfiles }
                    </div>
                </div>
            </div>
        )
    }
}
