import React from "react";
import { Icon } from "semantic-ui-react";

const Icons = ({ game }) => {
  const stringifyStars = value => {
    let stars = "★".repeat(value);
    if (value % 1) {
      stars += "½";
    }
    return stars;
  };

  const getEntryType = type => {
    switch (type) {
      case "F":
        return "check circle";
      case "P":
        return "play circle";
      case "R":
        return "redo";
      case "S":
        return "plus";
      case "A":
        return "times circle";
      default:
        return null;
    }
  };

  return (
    <p className="activity-icons">
      {game.rating && (
        <span className="rating">{stringifyStars(game.rating)}</span>
      )}
      <Icon name={getEntryType(game.entry_type)} />
      {game.liked && <Icon name="heart" />}
      {game.review && <Icon name="align left" />}
    </p>
  );
};

export default Icons;
