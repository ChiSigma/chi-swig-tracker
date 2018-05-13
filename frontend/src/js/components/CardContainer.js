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
            show: false,
            profiles: [1, 2, 3, 4]
        }; // main
        
        this.activeProfile = 1;

        this.handleShow = this.handleShow.bind(this);
        this.handleClose = this.handleClose.bind(this);
    }

    handleClose() {
        this.setState({ show: false })
    }

    handleShow() {
        console.log('showing the modal');
        this.setState({ show: true })
    }

    changeActiveProfile(activeProfile) {
        console.log('changing active profile!');
        this.activeProfile = activeProfile;
        this.handleShow();
    }
    
    render() {
        const miniProfiles = this.state.profiles.map((activeProfile) =>
            <div className="m-4">
                <MiniProfileCard changeActiveProfile={ this.changeActiveProfile.bind(this) } activeProfile={ activeProfile } />
            </div>
        );
        const modal = this.state.show ? (
            <div className="d-block modal">
                <div className="bg-gray-transparent modal-backdrop h-100 d-flex justify-content-center align-items-center" onClick={ this.handleClose }>
                    <div className="flip-container">
                        <ProfileCard profileID={ this.activeProfile } />
                    </div>
                </div>
            </div>
        ) : (
            console.log('hiding the modal!')
        );

        return (
            <div className="container pt-4">
                { modal }
                <div className="row">
                    <div className="d-flex align-items-baseline justify-content-center flex-wrap">
                            { miniProfiles }
                    </div>
                </div>
            </div>
        )
    }
}
