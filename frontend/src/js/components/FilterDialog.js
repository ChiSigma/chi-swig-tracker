import React from 'react';
import PropTypes from 'prop-types';
import Button from '@material-ui/core/Button';
import { withStyles } from '@material-ui/core/styles';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';
import FilterDropdowns from './FilterDropdowns';
import ProgressBar from './ProgressBar';

const styles = theme => ({
  paper: {
    overflowY: 'visible'
  },
  container: {
    display: 'flex',
    flexWrap: 'wrap'
  },
  formControl: {
    margin: theme.spacing.unit,
    minWidth: 120,
  },
});

class DialogSelect extends React.Component {
  constructor(props) {
    super(props);
    this.appState = () => { return this.props.context.state };
    this.state = {
      open: false,
      groups: props.context.state.groups.join(','),
      drinkers: props.context.state.drinkers.join(','),
      profileType: props.context.state.profileType,
      loading: false,
      version: {}
    };
  }

  handleClickOpen = () => {
    this.setState({
      open: true,
      groups: this.appState().groups.join(','),
      drinkers: this.appState().drinkers.join(','),
      profileType: this.appState().profileType,
      version: this.appState().version
    });
  };

  handleClose = () => {
    this.setState({ open: false });
  };

  handleSave = async () => {
    const drinkers = this.state.profileType === 'drinkers' && this.state.drinkers ? this.state.drinkers.split(',').map(id => (parseInt(id))) : []
    const groups = this.state.groups && this.state.groups ? this.state.groups.split(',').map(id => (parseInt(id))) : []
    const profileType = this.state.profileType;

    await this.appState().updateFilters({ drinkers, groups, profileType });
    this.setState({ open: false });
  };

  render() {
    const { classes } = this.props;
    const loadingOverlay = this.state.loading ? (
                <div id="card-container-loading">
                    <ProgressBar />
                </div>
            ) : (
                console.log('finished loading!')
            );
    const limitedWarning = this.state.version.is_limited ? (
                <span className="scope-limit-warning">
                    <br />*current selection is limited due to privacy settings
                </span>
            ) : (
                console.log('filter scope is not limited')
            );

    return (
      <div className="filterDialog">
        <Button onClick={this.handleClickOpen}>Open filter dialog</Button>
        <Dialog
          disableBackdropClick
          disableEscapeKeyDown
          maxWidth="xs"
          fullWidth={ true }
          open={this.state.open}
          onClose={this.handleClose}
          classes={ {paper: classes.paper} }
        >
          <DialogTitle>Select the Desired Filters{ limitedWarning }</DialogTitle>
          { loadingOverlay }
          <DialogContent classes={ {root: classes.paper} }>
            <FilterDropdowns context={ this.props.context } updateParent={ this.setState.bind(this) } state={ this.state } />
          </DialogContent>
          <DialogActions>
            <Button onClick={this.handleClose} color="primary">
              Cancel
            </Button>
            <Button onClick={this.handleSave} color="primary">
              Ok
            </Button>
          </DialogActions>
        </Dialog>
      </div>
    );
  }
}

DialogSelect.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(DialogSelect);
