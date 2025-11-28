import { NextResponse } from "next/server";

type EntranceExamRequirement = {
  required: boolean;
  description?: string;
};

type LanguageRequirement = {
  required: boolean;
  min_score?: number;
};

type EnglishProficiencyRequirement = {
  toefl?: LanguageRequirement;
  ielts?: LanguageRequirement;
};

type ScholarshipInfo = {
  available: boolean;
  description?: string;
  types?: string[];
};

type UniversityRecord = {
  country: string;
  location: string;
  programs: string[];
  imageUrl?: string;
  requirements: {
    min_grade: number;
    preferred_subjects: string[];
    entrance_exam?: EntranceExamRequirement;
    english_proficiency?: EnglishProficiencyRequirement;
  };
  scholarships?: ScholarshipInfo;
};

const UNIVERSITY_DATABASE = {
  "Cambodia Academy of Digital Technology (CADT)": {
    country: "Cambodia",
    location: "Phnom Penh",
    programs: [
      "Computer Science",
      "Digital Technology",
      "Artificial Intelligence",
      "Data Science",
      "Cybersecurity",
      "Digital Business",
      "Telecommunications and Networking",
      "UX/UI Design",
      "Digital Design",
    ],
    imageUrl: "https://cadt.edu.kh/wp-content/uploads/2025/08/IMG_4219-copy-scaled.webp", 
    requirements: {
      min_grade: 75,
      preferred_subjects: ["math", "english"],
      entrance_exam: {
        required: true,
        description:
          "Entrance exam covering mathematics, English, and general knowledge",
      },
      english_proficiency: {
        ielts: { required: false },
        toefl: { required: false },
      },
    },
    scholarships: {
      available: true,
      description: "Merit-based and need-based scholarships available",
      types: ["Merit Scholarship", "Need-Based", "Technology Excellence"],
    },
  },

  "Royal University of Phnom Penh (RUPP)": {
    country: "Cambodia",
    location: "Phnom Penh",
    programs: [
      "Computer Science",
      "Mathematics",
      "Physics",
      "Chemistry",
      "Biology",
      "Business Administration",
      "Information Technology",
      "Social Sciences",
      "Foreign Languages",
      "Electrical Engineering",
      "Mechanical Engineering",
      "Civil Engineering",
      "Graphic Design",
    ],
    imageUrl:"https://academics-bucket-sj19asxm-prod.s3.ap-southeast-1.amazonaws.com/3268bdb3-39f2-4818-87cb-7939736f2740/0706543a-4a63-4a17-8aaf-210ebbfb558d.jpg",
    requirements: {
      min_grade: 70,
      preferred_subjects: ["math", "english"],
      entrance_exam: {
        required: true,
        description: "National entrance examination required",
      },
      english_proficiency: {
        ielts: { required: false },
        toefl: { required: false },
      },
    },
    scholarships: {
      available: true,
      description: "Government scholarships and merit-based awards",
      types: ["Government Scholarship", "Merit-Based", "Research Grant"],
    },
  },

  "Institute of Technology of Cambodia (ITC)": {
    country: "Cambodia",
    location: "Phnom Penh",
    programs: [
      "Civil Engineering",
      "Electrical Engineering",
      "Mechanical Engineering",
      "Industrial Engineering",
      "Computer Science",
      "Telecommunications",
      "Information Technology",
    ],
    imageUrl:"https://camtesol.org/Upload_s/ITC%203.jpg",
    requirements: {
      min_grade: 75,
      preferred_subjects: ["math", "physics"],
      entrance_exam: {
        required: true,
        description:
          "Technical entrance exam focusing on mathematics and physics",
      },
      english_proficiency: {
        ielts: { required: false },
        toefl: { required: false },
      },
    },
    scholarships: {
      available: true,
      description: "Engineering excellence scholarships available",
      types: ["Engineering Excellence", "Merit-Based"],
    },
  },

  "Phnom Penh International University (PPIU)": {
    country: "Cambodia",
    location: "Phnom Penh",
    programs: [
      "Business Administration",
      "Information Technology",
      "Engineering",
      "Education",
      "Computer Science",
    ],
    imageUrl:"https://i.ytimg.com/vi/_ppq6grlOXY/maxresdefault.jpg",
    requirements: {
      min_grade: 65,
      preferred_subjects: ["math", "english"],
      entrance_exam: {
        required: false,
      },
      english_proficiency: {
        ielts: { required: false },
        toefl: { required: false },
      },
    },
    scholarships: {
      available: true,
      description: "Merit-based scholarships available",
      types: ["Merit-Based"],
    },
  },

  "Western University": {
    country: "Cambodia",
    location: "Phnom Penh",
    programs: [
      "Business Administration",
      "Digital Marketing",
      "Information Technology",
      "Economics",
      "Computer Science",
    ],
    imageUrl: "https://westernuniversity.edu.kh/laravel-filemanager/photos/shares/map/map%20toul%20kork%20(1).png",
    requirements: {
      min_grade: 60,
      preferred_subjects: ["math", "english"],
      entrance_exam: {
        required: false,
      },
      english_proficiency: {
        ielts: { required: false },
        toefl: { required: false },
      },
    },
    scholarships: {
      available: true,
      description: "Various scholarship opportunities",
      types: ["Merit-Based", "Need-Based"],
    },
  },

  "Royal University of Law and Economics (RULE)": {
    country: "Cambodia",
    location: "Phnom Penh",
    programs: [
      "Law",
      "Economics",
      "Business Administration",
      "Accounting",
      "Finance",
      "International Business",
    ],
    imageUrl: "https://elbbl.rule.edu.kh/wp-content/uploads/2024/01/RULE-building-D.jpg",
    requirements: {
      min_grade: 65,
      preferred_subjects: ["english", "history"],
      entrance_exam: {
        required: true,
        description:
          "Entrance exam covering English, history, and general knowledge",
      },
      english_proficiency: {
        ielts: { required: false },
        toefl: { required: false },
      },
    },
    scholarships: {
      available: true,
      description: "Law and economics excellence scholarships",
      types: ["Law Excellence", "Economics Excellence", "Merit-Based"],
    },
  },

  "Build Bright University (BBU)": {
    country: "Cambodia",
    location: "Multiple campuses",
  
    programs: [
      "Information Technology",
      "Business Administration",
      "Engineering",
      "Education",
      "Public Administration",
      "Computer Science",
    ],
    imageUrl: "https://bbu-webiste-space.sgp1.cdn.digitaloceanspaces.com/campus/pp/logo/20250816071156_bd0691f6fd091331c1bd902546ed881652946d43cc827c9d0c408c4b96cd8ffe.webp",     
    requirements: {
      min_grade: 60,
      preferred_subjects: ["math", "english"],
      entrance_exam: {
        required: false,
      },
      english_proficiency: {
        ielts: { required: false },
        toefl: { required: false },
      },
    },
    scholarships: {
      available: true,
      description: "Scholarships for outstanding students",
      types: ["Merit-Based", "Need-Based"],
    },
  },

  "University of Cambodia (UC)": {
    country: "Cambodia",
    location: "Phnom Penh",
    
    programs: [
      "Business Administration",
      "Information Technology",
      "International Relations",
      "Law",
      "Media Studies",
      "Education",
      "Computer Science",
      "Graphic Design",
    ],
    imageUrl: "https://uni24k.com/media/CACHE/images/unis/building_schools_u364e4ca0_772c4f1e/0b614424a3c23214ee21e9bca7778dbf.jpg",
    requirements: {
      min_grade: 65,
      preferred_subjects: ["math", "english"],
      entrance_exam: {
        required: false,
      },
      english_proficiency: {
        ielts: { required: false },
        toefl: { required: false },
      },
    },
    scholarships: {
      available: true,
      description: "Academic excellence and need-based scholarships",
      types: ["Academic Excellence", "Merit-Based", "Need-Based"],
    },
  },

  "American University of Phnom Penh (AUPP)": {
    country: "Cambodia",
    location: "Phnom Penh",
    
    programs: [
      "Business Administration",
      "Law",
      "Information Technology",
      "Civil Engineering",
      "Global Affairs",
      "Computer Science",
      "International Business",
      "Graphic Design",
      "Digital Media",
    ],
    imageUrl: "https://www.aupp.edu.kh/wp-content/uploads/Students-Life.jpg",
    requirements: {
      min_grade: 75,
      preferred_subjects: ["math", "english"],
      entrance_exam: {
        required: true,
        description: "English proficiency test and academic assessment",
      },
      english_proficiency: {
        ielts: { required: true, min_score: 6.0 },
        toefl: { required: true, min_score: 80 },
      },
    },
    scholarships: {
      available: true,
      description:
        "Comprehensive scholarship program including full and partial awards",
      types: [
        "Full Scholarship",
        "Partial Scholarship",
        "Merit-Based",
        "Need-Based",
      ],
    },
  },

  "National University of Management (NUM)": {
    country: "Cambodia",
    location: "Phnom Penh",

    programs: [
      "Business Administration",
      "Accounting",
      "Finance",
      "Marketing",
      "Management",
      "Tourism & Hospitality",
      "Economics",
    ],
    imageUrl: "https://numer.digital/public/faculties/MainSlide/num_front.jpg",
    requirements: {
      min_grade: 65,
      preferred_subjects: ["math", "english"],
      entrance_exam: {
        required: true,
        description: "Business and management aptitude test",
      },
      english_proficiency: {
        ielts: { required: false },
        toefl: { required: false },
      },
    },
    scholarships: {
      available: true,
      description: "Business excellence and management scholarships",
      types: ["Business Excellence", "Merit-Based"],
    },
  },

  "Royal University of Fine Arts (RUFA)": {
    country: "Cambodia",
    location: "Phnom Penh",
  
    programs: [
      "Fine Arts",
      "Architecture",
      "Archaeology",
      "Cultural Heritage",
      "Music",
      "Dance",
      "Traditional Arts",
      "Design",
      "Graphic Design",
      "UX/UI Design",
      "Visual Design",
    ],
    requirements: {
      min_grade: 60,
      preferred_subjects: ["english"],
      entrance_exam: {
        required: true,
        description: "Portfolio review and artistic aptitude test required",
      },
      english_proficiency: {
        ielts: { required: false },
        toefl: { required: false },
      },
    },
    scholarships: {
      available: true,
      description: "Arts excellence and cultural heritage scholarships",
      types: ["Arts Excellence", "Cultural Heritage", "Merit-Based"],
    },
  },

  "University of Health Sciences (UHS)": {
    country: "Cambodia",
    location: "Phnom Penh",
    
    programs: [
      "Medicine",
      "Pharmacy",
      "Dentistry",
      "Nursing",
      "Public Health",
      "Biomedical Sciences",
      "Health Administration",
    ],
    imageUrl: "https://uhs.edu.kh/internet/uhswebsite5/about/images/uhs.png",
    requirements: {
      min_grade: 80,
      preferred_subjects: ["biology", "chemistry", "math"],
      entrance_exam: {
        required: true,
        description:
          "Rigorous medical entrance examination covering sciences",
      },
      english_proficiency: {
        ielts: { required: false },
        toefl: { required: false },
      },
    },
    scholarships: {
      available: true,
      description: "Medical scholarships and government health sector funding",
      types: ["Medical Excellence", "Government Health Sector", "Merit-Based"],
    },
  },

  "Paññāsāstra University of Cambodia (PUC)": {
    country: "Cambodia",
    location: "Phnom Penh",
    
    programs: [
      "Business Administration",
      "International Relations",
      "Law",
      "Education",
      "Computer Science",
      "TESOL",
      "English Literature",
    ],
    imageUrl: "https://www.puc.edu.kh/wp-content/uploads/elementor/thumbs/TPP-r2atzmsbcurg41dyjzssruxyusj8x4rtvpcw35x0c4.jpg",
    requirements: {
      min_grade: 70,
      preferred_subjects: ["english", "math"],
      entrance_exam: {
        required: false,
      },
      english_proficiency: {
        ielts: { required: false },
        toefl: { required: false },
      },
    },
    scholarships: {
      available: true,
      description: "Academic excellence scholarships available",
      types: ["Academic Excellence", "Merit-Based"],
    },
  },

  "Paragon International University (Paragon.U)": {
    country: "Cambodia",
    location: "Phnom Penh",
    
    programs: [
      "Business Administration",
      "International Relations",
      "Data Science",
      "Computer Science",
      "Civil Engineering",
      "Architecture",
      "Information Technology",
      "UX/UI Design",
      "Digital Design",
    ],
    imageUrl: "https://academics-bucket-sj19asxm-prod.s3.ap-southeast-1.amazonaws.com/47268da4-7c59-4aa1-9d5d-1f94a31756af/feature-image.jpg",
    requirements: {
      min_grade: 70,
      preferred_subjects: ["math", "english"],
      entrance_exam: {
        required: false,
      },
      english_proficiency: {
        ielts: { required: true, min_score: 5.5 },
        toefl: { required: false },
      },
    },
    scholarships: {
      available: true,
      description: "International programs with scholarship opportunities",
      types: ["International Excellence", "Merit-Based", "Need-Based"],
    },
  },

  "University of Puthisastra (UP)": {
    country: "Cambodia",
    location: "Phnom Penh",
  
    programs: [
      "Medicine",
      "Dentistry",
      "Pharmacy",
      "Nursing",
      "Midwifery",
      "Public Health",
      "Health Sciences",
    ],
    imageUrl: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTK6aVBBRZKnaMiDj_49C-4UCtZkRAerTUQcw&s",
    requirements: {
      min_grade: 80,
      preferred_subjects: ["biology", "chemistry", "math"],
      entrance_exam: {
        required: true,
        description:
          "Medical entrance examination with focus on biology and chemistry",
      },
      english_proficiency: {
        ielts: { required: false },
        toefl: { required: false },
      },
    },
    scholarships: {
      available: true,
      description: "Health sciences scholarships and financial aid programs",
      types: ["Health Sciences Scholarship", "Merit-Based", "Need-Based"],
    },
  },

  "National Polytechnic Institute of Cambodia (NPIC)": {
    country: "Cambodia",
    location: "Phnom Penh",
    
    programs: [
      "Information Technology",
      "Engineering",
      "Multimedia",
      "Electronics",
      "Computer Science",
      "Technical Programs",
      "Graphic Design",
      "Digital Media Design",
    ],
    imageUrl:"https://academics-bucket-sj19asxm-prod.s3.ap-southeast-1.amazonaws.com/dd2414dc-584c-4704-91aa-29299535b232/feature-image.jpg",
    requirements: {
      min_grade: 70,
      preferred_subjects: ["math", "physics"],
      entrance_exam: {
        required: true,
        description: "Technical and polytechnic entrance examination",
      },
      english_proficiency: {
        ielts: { required: false },
        toefl: { required: false },
      },
    },
    scholarships: {
      available: true,
      description: "Technical excellence and polytechnic scholarships",
      types: ["Technical Excellence", "Polytechnic Scholarship", "Merit-Based"],
    },
  },

  "Rithypanha University (RHYU)": {
    country: "Cambodia",
    location: "Phnom Penh",
   
    programs: ["Information Technology", "Business Administration"],
    requirements: {
      min_grade: 70,
      preferred_subjects: ["math", "physics"],
      entrance_exam: {
        required: true,
        description: "Technical and polytechnic entrance examination",
      },
      english_proficiency: {
        ielts: { required: true, min_score: 5.5 },
        toefl: { required: false },
      },
    },
    scholarships: {
      available: false,
      description: "Technical excellence and polytechnic scholarships",
      types: ["Technical Excellence", "Polytechnic Scholarship", "Merit-Based"],
    },
  },


  Norton: {
    country: "Cambodia",
    location: "Phnom Penh",
   
    programs: [
      "Computer Science",
      "Information Technology",
      "Engineering",
      "Business Administration",
      "Education",
      "Graphic Design",
    ],
    imageUrl: "https://cdn.norton-u.com/nu/public_file/images/about/building.jpg",
    requirements: {
      min_grade: 70,
      preferred_subjects: ["math", "physics"],
      entrance_exam: {
        required: true,
        description: "Technical and polytechnic entrance examination",
      },
      english_proficiency: {
        ielts: { required: true, min_score: 5.5 },
        toefl: { required: false },
      },
    },
    scholarships: {
      available: true,
      description: "Technology and design focused scholarships",
      types: ["Technology Excellence", "Design Innovation", "Merit-Based"],
    },
  },
};

export async function GET() {
  try {
    const universities = Object.entries(UNIVERSITY_DATABASE).map(
      ([name, data]) => ({
        name,
        ...data,
      })
    );

    return NextResponse.json({ universities });
  } catch (error) {
    console.error("Error fetching universities:", error);
    return NextResponse.json(
      { error: "Failed to fetch universities" },
      { status: 500 }
    );
  }
}
