import React from "react"
import { useDispatch, useSelector } from "react-redux"
import { useEffect, useState } from "react"
import CoordinatorWithOutData from "./coordinatorProfile/modules/CoordinatorWithOutData/coordinatorWithOutData"
import CoordinatorWithData from "./coordinatorProfile/modules/coordinatorWithData/coordinatorWithData"
import { CoordinatorInfo } from "./api/coordinatorProfileApi"

function CoordinatorProfile(props) {
	const dispatch = useDispatch()
	const user = useSelector((state) => state.user.user)

	function getData() {
		const company = user.company
		const jobTitle = user.job_title
		const birthday = user.birthday
		const phoneNumber = user.phone_number

		if (!company || !jobTitle || !birthday || !phoneNumber) {
			return false
		} else {
			const data = [
				{ attribute: "Компания", value: company },
				{ attribute: "Должность", value: jobTitle },
				{ attribute: "Дата рождения", value: birthday },
				{ attribute: "Телефон", value: phoneNumber },
			]
			setData(data)
		}
	}

	useEffect(() => {
		new CoordinatorInfo(dispatch).getCoordinatorInfo()
		getData()
	}, [])

	const [data, setData] = useState(null)

	const without_data = <CoordinatorWithOutData />

	const with_data = <CoordinatorWithData data={data} />

	return <>{data ? with_data : without_data}</>
}

export default CoordinatorProfile
