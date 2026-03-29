/**
 * Adapted from Flatpickr Range plugin
 *
 * Author: https://github.com/flatpickr/flatpickr
 * Source code: https://github.com/flatpickr/flatpickr/blob/master/src/plugins/rangePlugin.ts
 */

function customDoubleNavPlugin(options = {}) {
    const config = { ...options };

    return function (fp) {
        let dateFormat = '',
            secondInput,
            _secondInputFocused,
            _prevDates;

        const createSecondInput = () => {
            if (config.input) {
                secondInput =
                    config.input instanceof Element
                        ? config.input
                        : window.document.querySelector(config.input);

                if (!secondInput) {
                    fp.config.errorHandler(
                        new Error('Invalid input element specified'),
                    );
                    return;
                }

                if (fp.config.wrap) {
                    secondInput = secondInput.querySelector('[data-input]');
                }
            } else {
                secondInput = fp._input.cloneNode();
                secondInput.removeAttribute('id');
                secondInput._flatpickr = undefined;
            }

            if (secondInput.value) {
                const parsedDate = fp.parseDate(secondInput.value);

                if (parsedDate) fp.selectedDates.push(parsedDate);
            }

            secondInput.setAttribute('data-fp-omit', '');

            if (fp.config.clickOpens) {
                fp._bind(secondInput, ['focus', 'click'], () => {
                    if (fp.selectedDates[1]) {
                        fp.latestSelectedDateObj = fp.selectedDates[1];
                        fp._setHoursFromDate(fp.selectedDates[1]);
                        fp.jumpToDate(fp.selectedDates[1]);
                    }

                    _secondInputFocused = true;
                    fp.isOpen = false;
                    fp.open(
                        undefined,
                        config.position === 'left' ? fp._input : secondInput,
                    );
                });

                fp._bind(fp._input, ['focus', 'click'], (e) => {
                    e.preventDefault();
                    fp.isOpen = false;
                    fp.open();
                });
            }

            if (fp.config.allowInput)
                fp._bind(secondInput, 'keydown', (e) => {
                    if (e.key === 'Enter') {
                        fp.setDate(
                            [fp.selectedDates[0], secondInput.value],
                            true,
                            dateFormat,
                        );
                        secondInput.click();
                    }
                });

            if (!config.input)
                fp._input.parentNode &&
                    fp._input.parentNode.insertBefore(
                        secondInput,
                        fp._input.nextSibling,
                    );
        };

        const plugin = {
            onParseConfig() {
                const newDate = new Date();
                const startDate = newDate.setMonth(newDate.getMonth() - 1);
                fp.config.now = startDate;
                console.log(
                    'config',
                    config,
                    'now date',
                    fp.config.now,
                    'startdate',
                    newDate.setMonth(newDate.getMonth() - 1),
                );

                fp.config.mode = 'single';
                fp.config.disableMobile = true;

                dateFormat = fp.config.altInput
                    ? fp.config.altFormat
                    : fp.config.dateFormat;
            },

            onReady() {
                createSecondInput();

                // Check if inputs have existing values BEFORE creating navigation
                const hasFirstValue = fp._input.value.trim() !== '';
                const hasSecondValue =
                    secondInput && secondInput.value.trim() !== '';
                let existingDates = null;

                if (hasFirstValue && hasSecondValue) {
                    const firstDate = fp.parseDate(fp._input.value);
                    const secondDate = fp.parseDate(secondInput.value);

                    if (firstDate && secondDate) {
                        existingDates = [firstDate, secondDate];
                    }

                    if (!firstDate && secondDate) {
                        existingDates = [null, secondDate];
                    }
                }

                // create navigation element
                const navContainer = document.createElement('div');
                navContainer.className = 'custom-nav';
                const navButtons = document.createElement('div');
                navButtons.className = 'flatpickr-nav-buttons';
                const documentFragment = document.createDocumentFragment();

                // Create navigation buttons dynamically
                config.buttons.forEach((buttonConfig) => {
                    const button = document.createElement('button');
                    button.setAttribute('id', buttonConfig.id);
                    button.innerHTML = buttonConfig.label;
                    button.addEventListener('click', function (e) {
                        e.preventDefault();
                        const newDate = new Date();
                        let secondDate = new Date();

                        if (buttonConfig.offset.months !== undefined) {
                            newDate.setMonth(
                                newDate.getMonth() + buttonConfig.offset.months,
                            );
                        }
                        if (buttonConfig.offset.days !== undefined) {
                            newDate.setDate(
                                newDate.getDate() + buttonConfig.offset.days,
                            );
                        }
                        if (buttonConfig.offset.fiscalYear === 'current') {
                            const fiscalMonth = buttonConfig.offset.month - 1;
                            const currentMonth = newDate.getMonth();

                            if (fiscalMonth <= currentMonth) {
                                // fiscal year start has passed
                                const offset = fiscalMonth - currentMonth;
                                newDate.setMonth(newDate.getMonth() + offset);
                            } else {
                                // fiscal year start has not yet passed
                                const year = newDate.getFullYear();
                                const fiscalYear = year - 1;

                                newDate.setMonth(fiscalMonth);
                                newDate.setFullYear(fiscalYear);
                                newDate.setDate(1);
                            }
                        }

                        if (buttonConfig.offset.fiscalYear === 'prev') {
                            const fiscalMonth = buttonConfig.offset.month - 1;
                            const currentMonth = newDate.getMonth();
                            const currentYear = newDate.getFullYear();

                            if (fiscalMonth <= currentMonth) {
                                // fiscal year start has passed
                                const fiscalYear = currentYear - 1;

                                newDate.setMonth(fiscalMonth);
                                newDate.setFullYear(fiscalYear);
                                newDate.setDate(1);

                                secondDate.setMonth(fiscalMonth);
                                secondDate.setDate(0);
                            } else {
                                // fiscal year start has not yet passed
                                const fiscalYear = currentYear - 2;

                                newDate.setMonth(fiscalMonth);
                                newDate.setFullYear(fiscalYear);
                                newDate.setDate(1);

                                secondDate.setMonth(fiscalMonth);
                                secondDate.setFullYear(fiscalYear + 1);
                                secondDate.setDate(0);
                            }
                        }

                        // Manually set both dates
                        const earlierDate =
                            newDate < secondDate ? newDate : secondDate;
                        const laterDate =
                            newDate < secondDate ? secondDate : newDate;

                        // Store in _prevDates
                        _prevDates = [earlierDate, laterDate];

                        // Update both inputs
                        fp._input.value = fp.formatDate(
                            earlierDate,
                            dateFormat,
                        );
                        secondInput.value = fp.formatDate(
                            laterDate,
                            dateFormat,
                        );

                        // Set the calendar to show the first date
                        fp.setDate(earlierDate, false);

                        // Redraw the calendar to show highlighting
                        fp.redraw();

                        if (config.closeOnSelect) {
                            fp.close();
                        }
                    });
                    documentFragment.appendChild(button);
                });

                navButtons.appendChild(documentFragment);
                navContainer.appendChild(navButtons);

                // Create calendar wrapper
                const calWrapper = document.createElement('div');
                calWrapper.className = 'cal-wrapper';
                const calChildren = Array.from(fp.calendarContainer.children);
                const wrapperFrag = document.createDocumentFragment();
                calChildren.forEach((child) => wrapperFrag.appendChild(child));
                calWrapper.appendChild(wrapperFrag);

                // Create inner wrapper
                const innerWrapper = document.createElement('div');
                innerWrapper.className = 'inner-wrapper';
                innerWrapper.appendChild(navContainer);
                innerWrapper.appendChild(calWrapper);

                fp.calendarContainer.appendChild(innerWrapper);
                fp.calendarContainer.style.width = config.width;

                fp.config.ignoredFocusElements.push(secondInput);
                if (fp.config.allowInput) {
                    fp._input.removeAttribute('readonly');
                    secondInput.removeAttribute('readonly');
                } else {
                    secondInput.setAttribute('readonly', 'readonly');
                }

                fp._bind(fp._input, 'focus', () => {
                    fp.latestSelectedDateObj = fp.selectedDates[0];
                    fp._setHoursFromDate(fp.selectedDates[0]);
                    _secondInputFocused = false;
                    fp.jumpToDate(fp.selectedDates[0]);
                });

                if (fp.config.allowInput) {
                    fp._bind(fp._input, 'keydown', (e) => {
                        if (e.key === 'Enter') {
                            fp.setDate(fp.parseDate(fp._input.value), true);
                        }
                    });
                }

                if (config.disableReset || existingDates) {
                    const datesToSet = (
                        existingDates || fp.selectedDates
                    ).filter(Boolean);
                    if (datesToSet.length) {
                        fp.setDate(datesToSet[0], false);
                    }
                    plugin.onValueUpdate(datesToSet);
                } else {
                    fp.selectedDates = [];
                    fp._input.value = '';
                    secondInput.value = '';
                    _prevDates = [];
                }

                fp.loadedPlugins.push('range');
            },
            onOpen() {
                fp.calendarContainer.style.width = 'fit-content';
                const monthsHeight =
                    fp.calendarContainer.querySelector(
                        '.flatpickr-months',
                    ).offsetHeight;
                const customNav =
                    fp.calendarContainer.querySelector('.custom-nav');
                const navTrueHeight =
                    fp.calendarContainer.offsetHeight - monthsHeight;
                customNav.style.height = `${navTrueHeight}px`;
            },

            onPreCalendarPosition() {
                if (_secondInputFocused) {
                    fp._positionElement = secondInput;
                    setTimeout(() => {
                        fp._positionElement = fp._input;
                    }, 0);
                }
            },

            onChange() {
                if (!fp.selectedDates.length) {
                    setTimeout(() => {
                        if (fp.selectedDates.length) return;

                        secondInput.value = '';
                        _prevDates = [];
                    }, 10);
                }

                if (_secondInputFocused) {
                    setTimeout(() => {
                        secondInput.focus();
                    }, 0);
                }
            },

            onDayCreate(dObj, dStr, fp, dayElem) {
                // Check if this day matches either of our stored dates
                const dayTime = new Date(dayElem.dateObj).setHours(0, 0, 0, 0);

                if (_prevDates) {
                    const firstDate = _prevDates[0];
                    const secondDate = _prevDates[1];

                    // Check if this day matches the first date
                    if (firstDate) {
                        const firstTime = new Date(firstDate).setHours(
                            0,
                            0,
                            0,
                            0,
                        );
                        if (dayTime === firstTime) {
                            dayElem.classList.add('selected');
                            dayElem.classList.add('startRange');
                        }
                    }

                    // Check if this day matches the second date
                    if (secondDate) {
                        const secondTime = new Date(secondDate).setHours(
                            0,
                            0,
                            0,
                            0,
                        );
                        if (dayTime === secondTime) {
                            dayElem.classList.add('selected');
                            dayElem.classList.add('endRange');
                        }
                    }

                    // Highlight range between dates if both exist
                    if (firstDate && secondDate) {
                        const first = new Date(firstDate).setHours(0, 0, 0, 0);
                        const second = new Date(secondDate).setHours(
                            0,
                            0,
                            0,
                            0,
                        );
                        const min = Math.min(first, second);
                        const max = Math.max(first, second);

                        if (dayTime > min && dayTime < max) {
                            dayElem.classList.add('inRange');
                        }
                    }
                }
            },

            onDestroy() {
                if (!config.input)
                    secondInput.parentNode &&
                        secondInput.parentNode.removeChild(secondInput);
            },

            onValueUpdate(selDates) {
                if (!secondInput) return;

                // In single mode, selDates will only have one date
                // We need to manually track both dates

                // Initialize _prevDates if it doesn't exist
                if (!_prevDates) {
                    _prevDates = [null, null];
                }

                // When a date is selected, store it in the appropriate position
                if (selDates.length === 1) {
                    const selectedDate = selDates[0];

                    if (_secondInputFocused) {
                        // Update second date
                        _prevDates[1] = selectedDate;
                        secondInput.value = fp.formatDate(
                            selectedDate,
                            dateFormat,
                        );
                    } else {
                        // Update first date
                        _prevDates[0] = selectedDate;
                        fp._input.value = fp.formatDate(
                            selectedDate,
                            dateFormat,
                        );
                    }

                    // Keep the display values in sync with our tracked dates
                    if (_prevDates[0]) {
                        fp._input.value = fp.formatDate(
                            _prevDates[0],
                            dateFormat,
                        );
                    }
                    if (_prevDates[1]) {
                        secondInput.value = fp.formatDate(
                            _prevDates[1],
                            dateFormat,
                        );
                    }

                    return;
                }

                // Handle clearing
                if (selDates.length === 0) {
                    if (_secondInputFocused) {
                        _prevDates[1] = null;
                        secondInput.value = '';
                    } else {
                        _prevDates[0] = null;
                        fp._input.value = '';
                    }
                }
            },
        };

        return plugin;
    };
}
