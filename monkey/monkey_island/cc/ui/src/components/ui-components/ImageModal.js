import React, {useState} from 'react';
import PropTypes from 'prop-types';
import {Button, Modal} from 'react-bootstrap';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faSearchPlus} from '@fortawesome/free-solid-svg-icons';


const ImageModal = (props) => {

  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <div className={'image-modal'}>
      <Button className={'image-modal-thumbnail'} onClick={() => setIsModalOpen(true)}>
        <FontAwesomeIcon icon={faSearchPlus} className={'image-modal-thumbnail-icon'}/>
        <Image src={props.image} thumbnail fluid/>
      </Button>
      <Modal show={isModalOpen}
             className={'image-modal-screen'}
             onHide={() => setIsModalOpen(false)}>
        <Modal.Body>
          <Image src={props.image} fluid />
        </Modal.Body>
      </Modal>
    </div>
  );
}

export default ImageModal;

ImageModal.propTypes = {
  image: PropTypes.string
}
