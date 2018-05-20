/**
 * Created by alexmelagrano on 5/9/18.
 */
import React from 'react';

export default class PrivacyButton extends React.Component {    
    async handleClick() {
        const newSetting = !this.props.isPublic;
        console.log(newSetting)
        await fetch('api/drinkers/' + this.props.myId + '/is_public', {
            method: 'PUT',
            credentials: 'same-origin',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({"is_public": newSetting})
        });

        window.location = '/';
    }

    render() {
        const buttonText = this.props.isPublic ? ("You're Public") : ("You're Private");
        const buttonType = this.props.isPublic ? 'btn-primary' : 'btn-warning'
        return(
            <div>
                <button className={ "btn " + buttonType } style={ {marginRight: "10px"} } type="button" onClick={this.handleClick.bind(this)} >{ buttonText }</button>
            </div>
        )
    }
}