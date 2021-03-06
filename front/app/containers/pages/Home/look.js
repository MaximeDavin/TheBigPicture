import { connect } from 'react-redux'
import React, { useEffect } from 'react'
import * as cst from '../../../constants'
import BigPictureList from '../../../components/BigPicture/list'
import NewBigPicture from '../../../components/BigPicture/new'
import BigPictureModal from '../../../components/BigPicture/modal'
import "./style.scss"


const HomeLook = ({ user, getBigPictures, count }) => {

  useEffect(() => {
    window.scrollTo(0, 0)
  }, [])

  return (
    <div className="vde container section">
      <BigPictureList
        name="home-page-bps-list"
        filter={(bp) => bp.kind == cst.SUBJECT && bp.private == false}
        parent={null}
        count={count}
        search={true}
        getPage={getBigPictures}
        loadFirstPage={true}
        emptyMessage={cst.labels.MSG_NO_SUBJECT}
        margin={0}
      />
    </div>
  )
}

export default HomeLook
