/**
 * Created by alexmelagrano on 5/9/18.
 */
import React from 'react';

import CardContainer from '../components/CardContainer';
import Navigation from '../components/Navigation';
import Subheader from '../components/Subheader';
import Footer from '../components/Footer';
import AdminContainer from '../components/admin/AdminContainer';

export default class Layout extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            view: 'dashboard'
        }
    }

    currentView() {
        return this.props.context.state.view;
    }

    componentDidUpdate(prevProps, prevState) {
        if (prevProps.context.state.view !== this.currentView()) {
            this.setState({ view: this.currentView() });
        }
    }
    
    render() {
        const toggleViews = function(component) {

            if (this.state.view === 'admin') {
                return (
                    <h1>YAyyyyyyyyyyyy</h1>
                )

            } else if (this.state.view === 'dashboard') {
                return ([
                    <Subheader context={ this.props.context }/>,
                    <CardContainer context={ this.props.context }/>,
                    <Footer context={ this.props.context }/>,
                ])
            }
        }.bind(this);

        return(
            <div>
                <Navigation />
                { toggleViews() }
            </div>
        )
    }
}