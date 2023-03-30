import React from "react"
import "./style/notice.scss"
import { useDispatch } from "react-redux"
import { NoticeService } from "../../services/noticeService"

function Notification({ message, id, status, ...props }) {
	const dispatch = useDispatch()

	let color = ""
	let colorIcon = ""

	switch (status) {
		case "info":
			color = "notice__content_info"
			colorIcon = "notice__content-icon-info"
			break
		case "error":
			color = "notice__content_error"
			colorIcon = "notice__content-icon-error"
			break
	}

	return (
		<div className={"notice__container"}>
			<div className={"notice__content " + color}>{message}</div>
			<div
				onClick={() => {
					new NoticeService(dispatch).deleteNotice(id)
				}}
				className={"notice__content-icon " + colorIcon}
			></div>
		</div>
	)
}

export default Notification
