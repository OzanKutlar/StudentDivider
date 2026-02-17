function getStudents(){
	let elementsMatrix = [];
	
	document.querySelectorAll('[id^="mod_assign_grading-"]').forEach(el => {
		let match = el.id.match(/^mod_assign_grading-\d+_r(\d+)$/);
		if (match) {
			let rowIndex = parseInt(match[1], 10);
			elementsMatrix[rowIndex] = [];
			
			Array.from(el.children).forEach((child, colIndex) => {
				elementsMatrix[rowIndex][colIndex] = child;
			});
		}
	});
	
	return elementsMatrix;
}

function downloadJavaFiles(matrix) {
    // Go through each student row
    matrix.forEach(student => {
        // The file upload column — might be index 6 or 7, depending on your layout
        let fileCell = student[6] || student[7];
        if (!fileCell) return;

        // Find all links inside the file upload cell
        const links = fileCell.querySelectorAll('a[href]');
        links.forEach(link => {
            // Check if it's a .java file
            if (link.href.includes('.java')) {
                console.log('Downloading:', link.href);
                
                // Simulate user click to trigger download
                const tempLink = document.createElement('a');
                tempLink.href = link.href;
                tempLink.target = '_blank';
                tempLink.download = '';
                document.body.appendChild(tempLink);
                tempLink.click();
                document.body.removeChild(tempLink);
            }
        });
    });
}


function processStudentMatrix(matrix) {
	const relevantIndexes = [1, 2, 3, 6, 7];
	
	let filteredMatrix = matrix.filter(student => student[4].innerText.startsWith("Submitted for grading"));
	// let filteredMatrix = matrix.filter(student => return true);
	
	let cleanedMatrix = filteredMatrix.map(student => relevantIndexes.map(index => student[index]));
	
	cleanedMatrix.forEach(student => {
		cleanStudent(student);
	});
	
	
	return cleanedMatrix;
}

function cleanStudent(arr) {
	const link = arr[4].querySelector('a');
	if (link) {
		arr[4] = link.href;
	} else {
		console.log('No <a> tag found in the provided element.');
	}
	
	// Name
	arr[0] = arr[0].innerText;
	
	// ID
	arr[1] = arr[1].innerText;
	
	// Email
	arr[2] = arr[2].innerText;

	// Time
	arr[3] = arr[3].innerText;
	
	
}

function downloadMatrixAsJson(matrix) {
	const replacer = (key, value) => {
		if (Array.isArray(value) && value.length === 5) {
			return {
				name: value[0],
				id: value[1],
				email: value[2],
				time: value[3],
				link: value[4]
			};
		}
		return value;
	};
	
	const jsonText = JSON.stringify(matrix, replacer, 2);
	
	const blob = new Blob([jsonText], { type: 'application/json' });
	
	const link = document.createElement('a');
	
	const url = URL.createObjectURL(blob);
	
	link.href = url;
	link.download = 'matrix.json';
	
	document.body.appendChild(link);
	link.click();
	
	document.body.removeChild(link);
	URL.revokeObjectURL(url);
}




temp = getStudents();
console.log(temp.length);
temp = processStudentMatrix(temp);

if (temp.length != 0) {
    // Download JSON summary
    downloadMatrixAsJson(temp);

    // Also trigger downloads of .java files
    // downloadJavaFiles(temp);
} else {
    alert("No submissions were found.");
}
