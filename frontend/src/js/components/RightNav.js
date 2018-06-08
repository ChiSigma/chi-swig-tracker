/**
 * Created by alexmelagrano on 5/9/18.
 */
import React from 'react';

import LoginButton from './LoginButton';
import PreferencesButton from './PreferencesButton';

export default class RightNav extends React.Component {
    constructor(props) {
        super(props);

        this.auth = () => { return this.props.context.auth };
        this.appState = () => { return this.props.context.state };
        this.state = {
            isLoggedIn: false,
            currentView: null,
            me: {}
        }
    }

    async componentWillMount() {
        const isLoggedIn = await this.auth().isLoggedIn();
        const currentView = this.appState().view;
        const me = await this.auth().me();
        this.setState({
            isLoggedIn: isLoggedIn,
            currentView: currentView,
            me: me
        })
    }

    render() {
        const toggle = this.state.isLoggedIn ? (
            <PreferencesButton currentView={ this.state.currentView } toggleView={ this.appState().toggleView } />
        ) : '';

        return(
            <div className="d-flex align-items-center">
                { toggle }
                <LoginButton isLoggedIn={this.state.isLoggedIn} />
            </div>
        )
    }
}
