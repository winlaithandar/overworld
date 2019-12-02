import React from "react";
import { connect } from "react-redux";
import { Divider, Icon, Message } from "semantic-ui-react";
import Cover from "../../../app/components/cover";
import { loadActivity } from "../../actions";
import ActivityIcons from "./ActivityIcons";
import "./styles.css";

class RecentActivity extends React.Component {
  componentDidMount() {
    this.props.loadActivity(this.props.username);
  }

  render() {
    const { activity } = this.props;
    return (
      <React.Fragment>
        <Divider horizontal>Recent Activity</Divider>
        {activity.length > 0 ? (
          <div className="recent-wrapper">
            {activity.map((g, i) => {
              return (
                <Cover
                  key={i}
                  imageId={g.game.cover_id}
                  size="small"
                  activity={<ActivityIcons game={g} />}
                />
              );
            })}
            {[...Array(5 - activity.length)].map((_, i) => (
              <div key={i} className="placeholder" />
            ))}
          </div>
        ) : (
          <Message className="no-content">
            <p>{this.props.username} has not been playing much...</p>
          </Message>
        )}
      </React.Fragment>
    );
  }
}

const mapStateToProps = state => ({
  activity: state.profile.activity
});

export default connect(mapStateToProps, { loadActivity })(RecentActivity);
