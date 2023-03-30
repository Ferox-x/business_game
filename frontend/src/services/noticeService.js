class Counter {
	static counter_id = 1

	static increaseCounter() {
		Counter.counter_id++
	}

	static getCounter() {
		return Counter.counter_id
	}
}

export class NoticeService {
	#infoStatus = "info"
	#errorStatus = "error"

	constructor(dispatch) {
		this.dispatch = dispatch
	}

	deleteNotice(noticeID) {
		this.dispatch({
			type: "DELETE_NOTICE",
			payload: { noticeID },
		})
	}

	addInfoNotice(message) {
		Counter.increaseCounter()
		const notice = this.createNoticeObject(message, this.#infoStatus)
		this.#addNotice(notice)
	}

	addErrorNotice(message) {
		Counter.increaseCounter()
		const notice = this.createNoticeObject(message, this.#errorStatus)
		this.#addNotice(notice)
	}

	#addNotice(noticeObject) {
		this.dispatch({
			type: "ADD_NOTICE",
			payload: noticeObject,
		})
		setTimeout(() => {
			this.deleteNotice(noticeObject.id)
		}, 5000)
	}

	createNoticeObject(message, status) {
		return {
			id: Counter.getCounter(),
			message: message,
			status: status,
		}
	}
}
