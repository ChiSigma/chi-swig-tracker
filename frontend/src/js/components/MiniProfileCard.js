/**
 * Created by alexmelagrano on 5/11/18.
 */
import React from 'react';

export default class MiniProfileCard extends React.Component {

    handleClick(e) {
        console.log('handling click to change active profile to: ' + this.props.activeProfile);
        this.props.changeActiveProfile(this.props.activeProfile);
    }

    render() {
        // TODO :: Pull in GroupName instead of hard coding it (doesn't yet exist)
        const profilePhoto = this.props.activeProfile["profile_photo"];
        const bio = this.props.activeProfile["bio_line"];
        const name = this.props.activeProfile["name"];
        
        return (
            <div className="mini-profile-card shadow-med px-2 py-1" onClick={ this.handleClick.bind(this) } >
                <div className="d-flex align-items-center my-2">
                    <div className="rounded mx-3">
                        <img src={ profilePhoto } alt="profile_photo" className="rounded-circle" width="70px" />
                    </div>
                    <div className="mr-3">
                        <h6 className="text-black-50 mb-1">Chi Sigma</h6>
                        <h5 className="font-weight-bold mb-0">{ name }</h5>
                    </div>
                </div>
                <div className="row px-5 mb-2 text-center">
                    <i className="text-black-50 small">{ bio }</i>
                </div>
            </div>
        )
    }
}
