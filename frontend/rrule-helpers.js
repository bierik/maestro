import isNull from 'lodash/isNull'
import isUndefined from 'lodash/isUndefined'
import DateTime from 'luxon/src/datetime'
import { RRule, RRuleSet } from 'rrule'

function applyExdates(source, target) {
  source.exdates().forEach((exdate) => target.exdate(exdate))
}

export function updateStart(rruleset, start) {
  const startDateTime = DateTime.fromJSDate(start).toUTC()

  const updateRruleset = update(rruleset, { dtstart: startDateTime.toJSDate() })
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

function applyReset(value, defaultValue) {
  if (isUndefined(value)) {
    return defaultValue
  }
  if (isNull(value)) {
    return undefined
  }
  return value
}

export function update(rruleset, { freq, dtstart, interval, until, count } = {}) {
  const updatedRruleset = new RRuleSet()
  applyExdates(rruleset, updatedRruleset)
  const currentRrule = rruleset.rrules()[0]
  const newRrule = new RRule({
    freq: applyReset(freq, currentRrule.options.freq),
    dtstart: applyReset(dtstart, currentRrule.options.dtstart),
    interval: applyReset(interval, currentRrule.options.interval),
    until: applyReset(until, currentRrule.options.until),
    count: applyReset(count, currentRrule.options.count),
  })
  updatedRruleset.rrule(newRrule)
  return updatedRruleset
}
