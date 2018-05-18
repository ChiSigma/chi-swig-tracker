/**
 * Created by alexmelagrano on 5/9/18.
 */
import React from 'react';

export default class LoginButton extends React.Component {
    constructor(props) {
        super(props);
    }
    
    handleAuthClick() {
        this.props.isLoggedIn ? window.location = '/auth/logout' : window.location = '/auth/login';
    }

    render() {
        const buttonText = this.props.isLoggedIn ? ('Log Out') : ('Log In');
        const buttonType = this.props.isLoggedIn ? 'btn-danger' : 'btn-secondary'
        return(
            <div>
                <button className={ "btn " + buttonType } type="button" onClick={this.handleAuthClick.bind(this)} >{ buttonText }</button>
            </div>
        )
    }
}