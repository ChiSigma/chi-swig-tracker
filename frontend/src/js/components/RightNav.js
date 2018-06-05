/**
 * Created by alexmelagrano on 5/9/18.
 */
import React from 'react';

import LoginButton from './LoginButton';
import PrivacyButton from './PrivacyButton';

export default class RightNav extends React.Component {
    constructor(props) {
        super(props);

        this.auth = props.context.auth;
        this.state = {
            isLoggedIn: false,
            isPublic: false,
            me: {}
        }
    }

    async componentWillMount() {
        const isLoggedIn = await this.auth.isLoggedIn();
        const isPublic = await this.auth.myPrivacySetting();
        const me = await this.auth.me();
        this.setState({
            isLoggedIn: isLoggedIn,
            isPublic: isPublic,
            me: me
        })
    }

    render() {
        const toggle = this.state.isLoggedIn ? (
            <PrivacyButton isPublic={this.state.isPublic} myId={this.state.me.id} />
        ) : '';

        return(
            <div className="d-flex align-items-center">
                { toggle }
                <LoginButton isLoggedIn={this.state.isLoggedIn} />
            </div>
        )
    }
}
