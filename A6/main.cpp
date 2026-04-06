#include<bits/stdc++.h>
using namespace std;

int getValidInput(string question) {
    int value;

    while(true) {
        cout << question;
        cin >> value;

        if(cin.fail()) {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << "Invalid input. Please enter a number between 1 and 5.\n";
            continue;
        }

        if(value >= 1 && value <= 5)
            return value;

        cout << "Input must be between 1 and 5. Try again.\n";
    }
}

void askQuestions(double &productivity, double &quality, double &teamwork, double &attendance, double &initiative) {

    // PRODUCTIVITY (3 questions)
    int p1 = getValidInput("Completes assigned tasks on time (1-5): ");
    int p2 = getValidInput("Handles workload efficiently (1-5): ");
    int p3 = getValidInput("Maintains consistent output (1-5): ");

    productivity = (p1 + p2 + p3) / 3.0;

    // QUALITY (3 questions)
    int q1 = getValidInput("Accuracy of work (1-5): ");
    int q2 = getValidInput("Attention to detail (1-5): ");
    int q3 = getValidInput("Follows company standards (1-5): ");

    quality = (q1 + q2 + q3) / 3.0;

    // TEAMWORK (3 questions)
    int t1 = getValidInput("Cooperates with colleagues (1-5): ");
    int t2 = getValidInput("Shares knowledge with team (1-5): ");
    int t3 = getValidInput("Supports team goals (1-5): ");

    teamwork = (t1 + t2 + t3) / 3.0;

    // ATTENDANCE (2 questions)
    int a1 = getValidInput("Punctuality (1-5): ");
    int a2 = getValidInput("Regular attendance (1-5): ");

    attendance = (a1 + a2) / 2.0;

    // INITIATIVE (3 questions)
    int i1 = getValidInput("Takes responsibility for tasks (1-5): ");
    int i2 = getValidInput("Shows problem-solving ability (1-5): ");
    int i3 = getValidInput("Suggests improvements (1-5): ");

    initiative = (i1 + i2 + i3) / 3.0;
}

double calculateBaseScore(double productivity, double quality, double teamwork, double attendance, double initiative) {

    double score =
        productivity * 0.30 +
        quality * 0.25 +
        teamwork * 0.20 +
        attendance * 0.15 +
        initiative * 0.10;

    return score * 20;
}

double applyExpertRules(double percentage, double productivity, double quality, double teamwork, double attendance, double initiative) {

    if(attendance == 5) percentage += 3;

    if(teamwork <= 2) percentage -= 5;

    if(productivity >= 4 && quality >= 4) percentage += 5;

    if(initiative <= 2) percentage -= 3;

    if(percentage > 100) percentage = 100;

    if(percentage < 0) percentage = 0;

    return percentage;
}

string getRating(double percentage) {

    if(percentage >= 90) return "Outstanding";
    else if(percentage >= 80) return "Excellent";
    else if(percentage >= 70) return "Very Good";
    else if(percentage >= 60) return "Good";
    else if(percentage >= 50) return "Average";
    else return "Needs Improvement";
}

void giveAdvice(double percentage) {

    cout << "Advice: ";

    if(percentage >= 90) cout << "Promotion Recommended\n";
    else if(percentage >= 70) cout << "Eligible for Bonus\n";
    else if(percentage >= 50) cout << "Performance Improvement Suggested\n";
    else cout << "Training Required\n";
}

int main() {

    cout << "EMPLOYEE PERFORMANCE EXPERT SYSTEM\n";
    cout << "----------------------------------\n";

    int n;
    cout << "Enter number of employees: ";
    cin >> n;

    for(int i = 1; i <= n; i++) {

        cout << "\nEvaluating Employee " << i << endl;

        double productivity, quality, teamwork, attendance, initiative;

        askQuestions(productivity, quality, teamwork, attendance, initiative);

        double percentage = calculateBaseScore(productivity, quality, teamwork, attendance, initiative);

        percentage = applyExpertRules(percentage, productivity, quality, teamwork, attendance, initiative);

        string rating = getRating(percentage);

        cout << "\nFinal Score: " << percentage << "%\n";
        cout << "Rating: " << rating << endl;

        giveAdvice(percentage);
    }

    return 0;
}