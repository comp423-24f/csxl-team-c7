export enum FormFieldType {
  SHORT_TEXT,
  LONG_TEXT,
  DROP_DOWN,
  NUMBER
}

export interface ApplicationFormField {
  name: string;
  title: string;
  description: string;
  fieldType: FormFieldType;
  required: boolean;
  dropdownItems?: string[];
}

export const ORGANIZATION_APPLICATION_FORM: ApplicationFormField[] = [
  {
    name: 'interest_statement',
    title: 'Why are you interested in joining?',
    description:
      'Please describe your interest in joining this organization. What do you hope to contribute and gain from membership?',
    fieldType: FormFieldType.LONG_TEXT,
    required: true
  },
  {
    name: 'experience',
    title: 'Relevant Experience',
    description:
      'Describe any relevant experience or skills you would bring to the organization.',
    fieldType: FormFieldType.LONG_TEXT,
    required: true
  },

  {
    name: 'expected_graduation',
    title: 'Expected Graduation',
    description: 'When do you expect to graduate?',
    fieldType: FormFieldType.DROP_DOWN,
    dropdownItems: [
      '2024 - Fall',
      '2025 - Spring',
      '2025 - Fall',
      '2026 - Spring',
      '2026 - Fall',
      '2027 - Spring',
      '2027 - Fall',
      'Later'
    ],
    required: true
  },
  {
    name: 'program_pursued',
    title: 'Program of Study',
    description: 'What is your current or intended major/minor?',
    fieldType: FormFieldType.DROP_DOWN,
    dropdownItems: [
      'CS Major (BS)',
      'CS Major (BA)',
      'CS Minor',
      'Other (Please specify in Additional Information)'
    ],
    required: true
  },
  {
    name: 'additional_info',
    title: 'Additional Information',
    description:
      'Is there anything else you would like us to know about your application?',
    fieldType: FormFieldType.LONG_TEXT,
    required: false
  }
];
