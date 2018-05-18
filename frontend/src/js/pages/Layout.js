/**
 * Created by alexmelagrano on 5/9/18.
 */
import React from 'react';

import CardContainer from '../components/CardContainer';
import Navigation from '../components/Navigation';
import Subheader from '../components/Subheader';
import AppContext from '../app-context';

export default class Layout extends React.Component {
    constructor() {
        super();
    }
    
    render() {
        return(
            <div>
                <Navigation />
                <AppContext.Consumer>
                    {(context) => ([
                        <Subheader context={ context }/>,
                        <CardContainer context={ context }/>
                    ])}
                </ AppContext.Consumer>
                <p>[footer]</p>
            </div>
        )
    }
}