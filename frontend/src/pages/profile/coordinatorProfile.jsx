import React from "react"
import { useDispatch } from "react-redux"
import { useEffect, useState } from "react"
import CoordinatorWithOutData from "./coordinatorProfile/modules/CoordinatorWithOutData/coordinatorWithOutData"
import CoordinatorWithData from "./coordinatorProfile/modules/coordinatorWithData/coordinatorWithData"
import { CoordinatorInfo } from "./api/coordinatorProfileApi"

function CoordinatorProfile(props) {
	const dispatch = useDispatch()

	const [data, setData] = useState([])

	function getData(data) {
		const company = data.company
		const jobTitle = data.job_title
		const birthday = data.birthday
		const phoneNumber = data.phone_number

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

	const without_data = <CoordinatorWithOutData />

	const with_data = <CoordinatorWithData data={data} />

	useEffect(() => {
		new CoordinatorInfo(dispatch).getCoordinatorInfo().then((response) => {
			getData(response.data)
		})
	}, [])

	return <>{data !== [] ? with_data : without_data}</>
}

export default CoordinatorProfile
