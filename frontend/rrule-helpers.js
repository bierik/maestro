import DateTime from 'luxon/src/datetime'
import { RRule, RRuleSet } from 'rrule'

function applyExdates(source, target) {
  source.exdates().forEach((exdate) => target.exdate(exdate))
}

export function updateStart(rruleset, start) {
  const startDateTime = DateTime.fromJSDate(start).toUTC()
  const rrule = rruleset.rrules()[0]

  const updatedDtStart = DateTime.fromJSDate(rrule.options.dtstart)
    .toUTC()
    .set({
      hours: startDateTime.hour,
      minutes: startDateTime.minute,
    })
    .toJSDate()

  const updateRruleset = update(rruleset, { dtstart: updatedDtStart })
  rruleset.exdates().forEach((exdate) => {
    const updatedExdate = DateTime.fromJSDate(exdate)
      .toUTC()
      .set({
        hours: startDateTime.hour,
        minute: startDateTime.minute,
      })
      .toJSDate()
    updateRruleset.exdate(updatedExdate)
  })
  return updateRruleset
}

export function exclude(rruleset, exclude) {
  rruleset.exdate(DateTime.fromJSDate(exclude).toUTC().toJSDate())
  return rruleset
}

export function until(rruleset, until) {
  const updatedRruleset = new RRuleSet()
  applyExdates(rruleset, updatedRruleset)
  const untilRule = DateTime.fromJSDate(until).toUTC().set({ hours: 0, minutes: 0 }).toJSDate()
  return update(rruleset, { until: untilRule })
}

export function update(rruleset, { freq, dtstart, interval, until } = {}) {
  const updatedRruleset = new RRuleSet()
  applyExdates(rruleset, updatedRruleset)
  const currentRrule = rruleset.rrules()[0]
  const newRrule = new RRule({
    freq: freq || currentRrule.options.freq,
    dtstart: dtstart || currentRrule.options.dtstart,
    interval: interval || currentRrule.options.interval,
    until: until || currentRrule.options.until,
  })
  updatedRruleset.rrule(newRrule)
  return updatedRruleset
}
