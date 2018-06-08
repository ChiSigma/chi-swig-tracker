/**
 * Created by alexmelagrano on 5/9/18.
 */
import React from 'react';

export default class PreferencesButton extends React.Component {    
    constructor(props) {
        super(props);
        this.state = {
            currentView: this.props.currentView
        }
    }

    handleClick() {
        this.setState({ currentView: this.props.toggleView() })
    }

    render() {
        const buttonText = this.state.currentView === 'admin' ? ("Go to Dashboard") : ("Edit Preferences");
        const buttonType = this.state.currentView === 'admin' ? 'btn-primary' : 'btn-warning'
        return(
            <div>
                <button className={ "btn " + buttonType } style={ {marginRight: "10px"} } type="button" onClick={this.handleClick.bind(this)} >{ buttonText }</button>
            </div>
        )
    }
}