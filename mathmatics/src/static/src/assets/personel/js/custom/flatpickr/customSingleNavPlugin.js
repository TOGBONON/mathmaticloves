function customSingleNavPlugin(options = {}) {
    const config = { ...options }

	return function(fp) {
		return {
            onParseConfig: function() {
                const newDate = new Date();
                const startDate = newDate.setMonth(newDate.getMonth() - 1)
                
                fp.config.now = startDate
            },
			onReady: function(selectedDates, dateStr, instance) {
				// create navigation element
				const navContainer = document.createElement('div');
                navContainer.className = 'custom-nav';
                const navButtons = document.createElement('div');
                navButtons.className = 'flatpickr-nav-buttons';
                const documentFragment = document.createDocumentFragment();

                // Create buttons dynamically
				config.buttons.forEach(buttonConfig => {
                    const button = document.createElement('button');
                    button.setAttribute('id', buttonConfig.id);
                    button.innerHTML = buttonConfig.label;
                    button.addEventListener('click', function(e) {
                        e.preventDefault();
                        const newDate = new Date();
                        
                        if (buttonConfig.offset.months !== undefined) {
                            newDate.setMonth(newDate.getMonth() + buttonConfig.offset.months);
                        }
                        if (buttonConfig.offset.days !== undefined) {
                            newDate.setDate(newDate.getDate() + buttonConfig.offset.days);
                        }
                        
                        instance.setDate(newDate, false, 'YYYY-MM-DD');
                        
                        if (config.closeOnSelect) {
                            instance.close();
                        }
                    });
                    documentFragment.appendChild(button);
                });
				
				navButtons.appendChild(documentFragment);
                navContainer.appendChild(navButtons);
                
                // Create calendar wrapper
                const calWrapper = document.createElement('div');
                calWrapper.className = 'cal-wrapper';
                const calChildren = Array.from(instance.calendarContainer.children);
                const wrapperFrag = document.createDocumentFragment();
                calChildren.forEach(child => wrapperFrag.appendChild(child));
                calWrapper.appendChild(wrapperFrag)
				
                // Create inner wrapper
                const innerWrapper = document.createElement('div');
                innerWrapper.className = 'inner-wrapper';
                innerWrapper.appendChild(navContainer);
                innerWrapper.appendChild(calWrapper);

                instance.calendarContainer.appendChild(innerWrapper);
                instance.calendarContainer.style.width = config.width;
			},
			onOpen: function(selectedDates, dateStr, instance) {
                instance.calendarContainer.style.width = 'fit-content';
                const monthsHeight = instance.calendarContainer.querySelector('.flatpickr-months').offsetHeight;
                const customNav = instance.calendarContainer.querySelector('.custom-nav');
                const navTrueHeight = instance.calendarContainer.offsetHeight - monthsHeight;
                customNav.style.height = `${navTrueHeight}px`;
            }
		}
	}
}