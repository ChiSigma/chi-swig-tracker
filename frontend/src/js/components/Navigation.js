/**
 * Created by alexmelagrano on 5/9/18.
 */
import React from 'react';
import AppContext from '../app-context';

import crestIcon from '../../assets/crestIcon.png';
import RightNav from './RightNav';

export default class Navigation extends React.Component {

    render() {
        return(
            <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
                <div className="container py-2">
                    <img src={ crestIcon } width="40px" alt="Chi_Sigma_Crest_Icon" />
                    <a className="navbar-brand ml-2 mr-auto mb-0 h1" target="blank" href="https://chisigma.co">Chi Swig</a>

                    <div>
                        <AppContext.Consumer>
                            {(context) => (
                                <RightNav context={ context } />
                            )}
                        </ AppContext.Consumer>
                    </div>
                </div>
            </nav>
        )
    }
}
