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
        // TODO :: const profilePhoto = this.props.activeProfile["profile_photo"];
        const profilePhoto = 'https://media.licdn.com/dms/image/C4E03AQHzXHptRd-cHg/profile-displayphoto-shrink_200_200/0?e=1531353600&v=beta&t=A5jkjzccz4PBvdNXggFFPwavsEorI6rXot2eRLn-iaY';
        // TODO :: const bio = this.props.activeProfile["bio_line"];
        const bio = 'I smell like lemonssss.';
        // TODO :: const name = this.props.activeProfile["name"];
        const name = 'Melons';
        
        return (
            <div className="mini-profile-card shadow-med px-2 py-1" onClick={ this.handleClick.bind(this) } >
                <div className="d-flex align-items-center my-2">
                    <div className="rounded mx-3">
                        <img src={ profilePhoto } alt="profile_photo" className="rounded-circle" width="70px" />
                    </div>
                    <div className="mr-3">
                        <h6 className="text-black-50 mb-1">First Name</h6>
                        <h5 className="font-weight-bold mb-0">{ name }</h5>
                    </div>
                </div>
                <div className="row px-5 mb-2">
                    <i className="text-black-50 small">{ bio }</i>
                </div>
            </div>
        )
    }
}
