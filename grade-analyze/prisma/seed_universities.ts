import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

const UNIVERSITY_DATABASE = {
  "Cambodia Academy of Digital Technology (CADT)": {
    country: "Cambodia",
    city: "Phnom Penh",
    availablePrograms: [
      "Software Engineering",
      "Data Science",
      "Cybersecurity",
      "Digital Business",
      "Telecommunications and Networking",
    ],
    imageUrl: "https://cadt.edu.kh/wp-content/uploads/2025/08/IMG_4219-copy-scaled.webp", 
    minGrade: 75,
    entranceExam: true,
    scholarshipAvailable: true,
    scholarshipDetail: "Merit-based and need-based scholarships available (Merit Scholarship, Need-Based, Technology Excellence)",
    locationMaps: "https://www.google.com/maps/place/Cambodia+Academy+of+Digital+Technology+(CADT)/@11.6530599,104.9068235,17z/data=!3m1!4b1!4m6!3m5!1s0x3109516bdea989b3:0x372d2c5e0e14b706!8m2!3d11.6530599!4d104.9116944!16s%2Fg%2F11byygmxw3?entry=ttu&g_ep=EgoyMDI1MTEzMC4wIKXMDSoASAFQAw%3D%3D",
    tuitionFee: null
  },

  "Royal University of Phnom Penh (RUPP)": {
    country: "Cambodia",
    city: "Phnom Penh",
    availablePrograms: [
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
    minGrade: 70,
    entranceExam: true,
    scholarshipAvailable: true,
    scholarshipDetail: "Government scholarships and merit-based awards",
    locationMaps: "https://www.google.com/maps/place/Royal+University+of+Phnom+Penh/@11.568676,104.8881668,17z/data=!3m1!4b1!4m6!3m5!1s0x3109519fe4077d69:0x20138e822e434660!8m2!3d11.568676!4d104.8907417!16s%2Fm%2F0278m39?entry=ttu&g_ep=EgoyMDI1MTEzMC4wIKXMDSoASAFQAw%3D%3D",
    tuitionFee: null
  },

  "Institute of Technology of Cambodia (ITC)": {
    country: "Cambodia",
    city: "Phnom Penh",
    availablePrograms: [
      "Civil Engineering",
      "Electrical Engineering",
      "Mechanical Engineering",
      "Industrial Engineering",
      "Computer Science",
      "Telecommunications",
      "Information Technology",
    ],
    imageUrl:"https://camtesol.org/Upload_s/ITC%203.jpg",
    minGrade: 75,
    entranceExam: true,
    scholarshipAvailable: true,
    scholarshipDetail: "Engineering excellence scholarships available",
    locationMaps: "https://www.google.com/maps/place/Institute+of+Technology+of+Cambodia/@11.5703975,104.8955108,17z/data=!3m1!4b1!4m6!3m5!1s0x3109517388680e15:0x63057e6682968f5!8m2!3d11.5703975!4d104.8980857!16zL20vMDZ5dmhz?entry=ttu&g_ep=EgoyMDI1MTEzMC4wIKXMDSoASAFQAw%3D%3D",
    tuitionFee: null
  },

  "Phnom Penh International University (PPIU)": {
    country: "Cambodia",
    city: "Phnom Penh",
    availablePrograms: [
      "Business Administration",
      "Information Technology",
      "Engineering",
      "Education",
      "Computer Science",
    ],
    imageUrl:"https://i.ytimg.com/vi/_ppq6grlOXY/maxresdefault.jpg",
    minGrade: 65,
    entranceExam: false,
    scholarshipAvailable: true,
    scholarshipDetail: "Merit-based scholarships available",
    locationMaps: null,
    tuitionFee: null
  },

  "Western University": {
    country: "Cambodia",
    city: "Phnom Penh",
    availablePrograms: [
      "Business Administration",
      "Digital Marketing",
      "Information Technology",
      "Economics",
      "Computer Science",
    ],
    imageUrl: "https://westernuniversity.edu.kh/laravel-filemanager/photos/shares/map/map%20toul%20kork%20(1).png",
    minGrade: 60,
    entranceExam: false,
    scholarshipAvailable: true,
    scholarshipDetail: "Various scholarship opportunities (Merit-Based, Need-Based)",
    locationMaps: null,
    tuitionFee: null
  },

  "Royal University of Law and Economics (RULE)": {
    country: "Cambodia",
    city: "Phnom Penh",
    availablePrograms: [
      "Law",
      "Economics",
      "Business Administration",
      "Accounting",
      "Finance",
      "International Business",
    ],
    imageUrl: "https://elbbl.rule.edu.kh/wp-content/uploads/2024/01/RULE-building-D.jpg",
    minGrade: 65,
    entranceExam: true,
    scholarshipAvailable: true,
    scholarshipDetail: "Law and economics excellence scholarships",
    locationMaps: null,
    tuitionFee: null
  },

  "Build Bright University (BBU)": {
    country: "Cambodia",
    city: "Multiple campuses",
    availablePrograms: [
      "Information Technology",
      "Business Administration",
      "Engineering",
      "Education",
      "Public Administration",
      "Computer Science",
    ],
    imageUrl: "https://bbu-webiste-space.sgp1.cdn.digitaloceanspaces.com/campus/pp/logo/20250816071156_bd0691f6fd091331c1bd902546ed881652946d43cc827c9d0c408c4b96cd8ffe.webp",     
    minGrade: 60,
    entranceExam: false,
    scholarshipAvailable: true,
    scholarshipDetail: "Scholarships for outstanding students",
    locationMaps: null,
    tuitionFee: null
  },

  "University of Cambodia (UC)": {
    country: "Cambodia",
    city: "Phnom Penh",
    availablePrograms: [
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
    minGrade: 65,
    entranceExam: false,
    scholarshipAvailable: true,
    scholarshipDetail: "Academic excellence and need-based scholarships",
    locationMaps: null,
    tuitionFee: null
  },

  "American University of Phnom Penh (AUPP)": {
    country: "Cambodia",
    city: "Phnom Penh",
    availablePrograms: [
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
    minGrade: 75,
    entranceExam: true,
    scholarshipAvailable: true,
    scholarshipDetail: "Comprehensive scholarship program including full and partial awards",
    locationMaps: null,
    tuitionFee: null
  },

  "National University of Management (NUM)": {
    country: "Cambodia",
    city: "Phnom Penh",
    availablePrograms: [
      "Business Administration",
      "Accounting",
      "Finance",
      "Marketing",
      "Management",
      "Tourism & Hospitality",
      "Economics",
    ],
    imageUrl: "https://numer.digital/public/faculties/MainSlide/num_front.jpg",
    minGrade: 65,
    entranceExam: true,
    scholarshipAvailable: true,
    scholarshipDetail: "Business excellence and management scholarships",
    locationMaps: null,
    tuitionFee: null
  },

  "Royal University of Fine Arts (RUFA)": {
    country: "Cambodia",
    city: "Phnom Penh",
    availablePrograms: [
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
    imageUrl: "https://i.pinimg.com/1200x/4f/1d/ef/4f1def2a4d49b27a764ec7d8b71ccce1.jpg",
    minGrade: 60,
    entranceExam: true,
    scholarshipAvailable: true,
    scholarshipDetail: "Arts excellence and cultural heritage scholarships",
    locationMaps: null,
    tuitionFee: null
  },

  "University of Health Sciences (UHS)": {
    country: "Cambodia",
    city: "Phnom Penh",
    availablePrograms: [
      "Medicine",
      "Pharmacy",
      "Dentistry",
      "Nursing",
      "Public Health",
      "Biomedical Sciences",
      "Health Administration",
    ],
    imageUrl: "https://uhs.edu.kh/internet/uhswebsite5/about/images/uhs.png",
    minGrade: 80,
    entranceExam: true,
    scholarshipAvailable: true,
    scholarshipDetail: "Medical scholarships and government health sector funding",
    locationMaps: null,
    tuitionFee: null
  },

  "Paññāsāstra University of Cambodia (PUC)": {
    country: "Cambodia",
    city: "Phnom Penh",
    availablePrograms: [
      "Business Administration",
      "International Relations",
      "Law",
      "Education",
      "Computer Science",
      "TESOL",
      "English Literature",
    ],
    imageUrl: "https://www.puc.edu.kh/wp-content/uploads/elementor/thumbs/TPP-r2atzmsbcurg41dyjzssruxyusj8x4rtvpcw35x0c4.jpg",
    minGrade: 70,
    entranceExam: false,
    scholarshipAvailable: true,
    scholarshipDetail: "Academic excellence scholarships available",
    locationMaps: null,
    tuitionFee: null
  },

  "Paragon International University (Paragon.U)": {
    country: "Cambodia",
    city: "Phnom Penh",
    availablePrograms: [
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
    minGrade: 70,
    entranceExam: false,
    scholarshipAvailable: true,
    scholarshipDetail: "International programs with scholarship opportunities",
    locationMaps: null,
    tuitionFee: null
  },

  "University of Puthisastra (UP)": {
    country: "Cambodia",
    city: "Phnom Penh",
    availablePrograms: [
      "Medicine",
      "Dentistry",
      "Pharmacy",
      "Nursing",
      "Midwifery",
      "Public Health",
      "Health Sciences",
    ],
    imageUrl: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTK6aVBBRZKnaMiDj_49C-4UCtZkRAerTUQcw&s",
    minGrade: 80,
    entranceExam: true,
    scholarshipAvailable: true,
    scholarshipDetail: "Health sciences scholarships and financial aid programs",
    locationMaps: null,
    tuitionFee: null
  },

  "National Polytechnic Institute of Cambodia (NPIC)": {
    country: "Cambodia",
    city: "Phnom Penh",
    availablePrograms: [
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
    minGrade: 70,
    entranceExam: true,
    scholarshipAvailable: true,
    scholarshipDetail: "Technical excellence and polytechnic scholarships",
    locationMaps: null,
    tuitionFee: null
  },

  "Norton": {
    country: "Cambodia",
    city: "Phnom Penh",
    availablePrograms: [
      "Computer Science",
      "Information Technology",
      "Engineering",
      "Business Administration",
      "Education",
      "Graphic Design",
    ],
    imageUrl: "https://cdn.norton-u.com/nu/public_file/images/about/building.jpg",
    minGrade: 70,
    entranceExam: true,
    scholarshipAvailable: true,
    scholarshipDetail: "Technology and design focused scholarships",
    locationMaps: null,
    tuitionFee: null
  }
};

async function main() {
  console.log('Start seeding universities...');
  
  // Clear existing universities
  await prisma.university.deleteMany({});
  
  for (const [name, data] of Object.entries(UNIVERSITY_DATABASE)) {
    const university = await prisma.university.create({
      data: {
        name: name,
        country: data.country,
        city: data.city,
        availablePrograms: data.availablePrograms,
        minGrade: data.minGrade,
        entranceExam: data.entranceExam,
        scholarshipAvailable: data.scholarshipAvailable,
        scholarshipDetail: data.scholarshipDetail,
        locationMaps: data.locationMaps,
        imageUrl: data.imageUrl,
        tuitionFee: data.tuitionFee
      }
    });
    console.log(`Created university: ${university.name}`);
  }
  
  console.log('Seeding finished.');
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
