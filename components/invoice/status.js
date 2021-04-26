const status = {
  CREATED: 'CREATED',
  SENT: 'SENT',
  PAYED: 'PAYED',
  ARCHIVED: 'ARCHIVED',
}

export default status

export const colors = {
  [status.CREATED]: 'created',
  [status.SENT]: 'sent',
  [status.PAYED]: 'payed',
  [status.ARCHIVED]: 'archived',
}
