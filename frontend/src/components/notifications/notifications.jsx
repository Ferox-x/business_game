import React from "react"
import Notification from "./notice"
import { useSelector } from "react-redux"
import "./style/notifications.scss"

function Notifications(props) {
	const notifications = useSelector((state) => state.notice)

	return (
		<div className="notifications_container">
			{notifications.map((notice, index) => {
				return (
					<Notification
						key={index}
						id={index}
						message={notice.message}
						status={notice.status}
					/>
				)
			})}
		</div>
	)
}

export default Notifications
