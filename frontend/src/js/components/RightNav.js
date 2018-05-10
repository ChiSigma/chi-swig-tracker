/**
 * Created by alexmelagrano on 5/9/18.
 */
import React from 'react';

import LoginButton from './LoginButton';

export default class RightNav extends React.Component {
    constructor() {
        super();
        this.isLoggedIn = false;
        this.isPublic = false;
    }

    render() {
        const toggle = this.isPublic ? (
            <span className="text-white mr-2">toggle button: on</span>
        ) : (
            <span className="text-white mr-2">toggle button: off</span>
        );

        return(
            <div className="d-flex align-items-center">
                { toggle }
                <LoginButton isLoggedIn={this.isLoggedIn} />
            </div>
        )
    }
}
