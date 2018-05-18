import React, {Component} from 'react';
import AppContext from '../app-context';

export default class AppProvider extends Component {
    constructor() {
        super();
        this.state = {
            currentUser: false,
            sortEventType: 1,
            sortTime: '*',
            isLoggedIn: async function() {
                const user = await this.state.me()
                return !!user.id;
            }.bind(this),
            isPublic: async function () {
                const user = await this.state.me()
                return !!user.is_public;
            }.bind(this),
            me: async function() {
                return await this.state.currentUser ? Promise.resolve(this.state.currentUser) : this.fetchMe();
            }.bind(this),
            updateSort: function(sortEventType=1, sortTime='*') {
                console.log({ sortEventType, sortTime })
                this.setState({ sortEventType, sortTime });
            }.bind(this)
        }
    }

    async fetchMe() {
        const userResp = await fetch('auth/me', {credentials: 'same-origin'})
        const user = await userResp.json();
        this.setState({currentUser: user});
        return user;
    }

    render() {
        return (
            <AppContext.Provider value={ this.state }>
                {this.props.children}
            </AppContext.Provider>
        );
    }
}