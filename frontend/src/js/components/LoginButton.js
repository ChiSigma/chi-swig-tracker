/**
 * Created by alexmelagrano on 5/9/18.
 */
import React from 'react';

export default class RightNav extends React.Component {
    constructor(props) {
        super(props);
        this.isLoggedIn = props.isLoggedIn;
    }
    handleAuthClick() {
        this.isLoggedIn ? (
            // TODO :: link to logout endpoint
            console.log('logout user')
        ) : (
            // TODO :: link to login endpoint
            console.log('login user')
        );
    }

    render() {
        const buttonText = this.isLoggedIn ? ('Log Out') : ('Log In');
        return(
            <div>
                <button className="btn btn-secondary" type="button" onClick={this.handleAuthClick.bind(this)} >{ buttonText }</button>
            </div>
        )
    }
}