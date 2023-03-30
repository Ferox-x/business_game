import { getAxiosInstanceAuth } from "../../../actions/axios_config"
import { NoticeApiBase } from "../../../utilits/baseApiClasses"

export class CreateGameApi extends NoticeApiBase {
	async getCoordinatorAttributes() {
		const axiosInstanceAuth = getAxiosInstanceAuth()

		return await axiosInstanceAuth
			.get("api/coordinator/attributes")
			.then((response) => {
				return response.data
			})
	}

	async postCreateGame(data) {
		const axiosInstanceAuth = getAxiosInstanceAuth()

		return await axiosInstanceAuth.post("api/game/start", { ...data }).then(() => {
			this.createNoticeSuccess("Игра успешно создана")
		})
	}
}
