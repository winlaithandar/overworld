import React from "react";
import PropTypes from "prop-types";
import { CoverWrapper, ImageLink, StyledCoverImage } from "./styles";

const Cover = ({ imageId, slug, size, activity }) => {
  const coverUrl = `https://images.igdb.com/igdb/image/upload/t_cover_big/${imageId}.jpg`;
  return (
    <CoverWrapper size={size}>
      <ImageLink to={`/games/${slug}`}>
        <StyledCoverImage src={coverUrl} rounded fluid />
      </ImageLink>
      {/* Render the activity icons in case there's any activity 
      for each game. Note: this is used only in the profile, in the 
      Recent Activity section */}
      {activity}
    </CoverWrapper>
  );
};

Cover.propTypes = {
  imageId: PropTypes.string.isRequired
};

export default Cover;
