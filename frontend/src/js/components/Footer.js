import React from 'react';

export default class Footer extends React.Component {
    render() {
        const trademarkClasses = this.props.context.state.autoRefresh ? "trademark-active" : "trademark"

        return(
            <footer className="footer footer-dark bg-dark">
                <div class="row">
                    <div class="col-4">
                        <p onClick={ this.props.context.state.toggleAutoRefresh } className={ trademarkClasses }>❤ Chi Sigma</p>
                    </div>
                    <div class="col-4">
                        <div class="text-center white-icons social-icons">
                            <a href="https://www.facebook.com/chisigma" target="_blank"><i class="fab fa-facebook social"></i></a>
                            <a href="https://www.instagram.com/chi.mfckn.sigma" target="_blank"><i id="social-inst" class="fab fa-instagram"></i></a>
                            <a href="mailto:info@chisigma.co" target="_blank"><i id="social-em" class="fa fa-envelope-square social"></i></a>
                        </div>
                    </div>
                    <div id="github-help-container" class="col-4"><a id="github-help" target="_blank" href="https://github.com/ChiSigma/chi-swig-tracker/blob/master/README.md">Need Help?</a></div>
                </div>
            </footer>
        )
    }
}
