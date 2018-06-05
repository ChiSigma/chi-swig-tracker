import React from 'react';

export default class Footer extends React.Component {
    render() {
        const trademarkClasses = this.props.context.state.autoRefresh ? "trademark-active" : "trademark"

        return(
            <footer className="footer footer-dark bg-dark">
                <p onClick={ this.props.context.state.toggleAutoRefresh } className={ trademarkClasses }>© 2018 Chi Sigma</p>
            </footer>
        )
    }
}
