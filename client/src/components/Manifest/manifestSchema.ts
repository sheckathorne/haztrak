import { rcraPhoneSchema, rcraSite } from 'components/RcraSite';
import { z } from 'zod';

/**
 * Used to specify whether a handler is a generator, transporter, or
 * designated receiving facility (AKA Treatment, Storage and Disposal Facility or TSDF for short).
 */
export const HandlerType = z.enum(['generator', 'designatedFacility', 'transporter']);
export type HandlerTypeEnum = z.infer<typeof HandlerType>;
export const paperSignatureSchema = z.object({
  printedName: z.string(),
  signatureDate: z.string(),
});
/**
 * Schema for signer of a hazardous waste manifest
 */
const signerSchema = z.object({
  /**
   * User's RCRAInfo username
   */
  userId: z.string().optional(),
  firstName: z.string().optional(),
  middleInitial: z.string().optional(),
  lastName: z.string().optional(),
  phone: rcraPhoneSchema.optional(),
  email: z.string().optional(),
  companyName: z.string().optional(),
  contactType: z.enum(['Email', 'Text', 'Voice']),
});
/**
 * EPA's RCRAInfo electronic signature schema
 */
export const electronicSignatureSchema = z.object({
  signer: signerSchema.optional(),
  signatureDate: z.date().optional(),
  /**
   * Object representing metadata on a printable, human friendly, version of the manifest
   * ToDo: see the USEPA/e-Manifest documentation on GitHub
   */
  humanReadableDocument: z.any().optional(),
});
export const handlerSchema = rcraSite.extend({
  paperSignatureInfo: paperSignatureSchema.optional(),
  electronicSignaturesInfo: electronicSignatureSchema.array().optional(),
  /**
   * Property on by back end to signify whether the handler has signed
   */
  signed: z.boolean().optional(),
});
/**
 * The Handler extends the RcraSite schema and adds manifest specific data
 */
export type Handler = z.infer<typeof handlerSchema>;
/**
 * The Signature that appears on paper versions of the manifest
 */

export const transporterSchema = handlerSchema.extend({
  order: z.number(),
  manifest: z.number().optional(),
});

/**
 *  The Transporter type extends the Handler schema and adds transporter
 *  specific data, such as their order on the manifest
 */
export type Transporter = z.infer<typeof transporterSchema>;

export type PaperSignature = z.infer<typeof paperSignatureSchema>;
/**
 * A signer of a hazardous waste manifest
 */
export type Signer = z.infer<typeof signerSchema>;
/**
 * RCRAInfo electronic signature definition
 */
export type ElectronicSignature = z.infer<typeof electronicSignatureSchema>;
export const manifestSchema = z
  .object({
    manifestTrackingNumber: z.string().optional(),
    /**
     * The date-time the manifest was created in the e-Manifest system.
     * Managed by EPA's systems.
     */
    createdDate: z.string().optional(),
    /**
     * The last date-time manifest was updated in the e-Manifest system.
     * Managed by EPA's systems.
     */
    updatedDate: z.string().optional(),
    /**
     * The date-time the hazardous waste shipment departed (was signed by) the generator.
     * Managed by EPA's systems, but not present on pre-shipment manifests.
     */
    shippedDate: z.string().optional(),
    import: z.boolean().optional(),
    rejection: z.boolean().optional(),
    potentialShipDate: z
      .string()
      .optional()
      .transform((val) => {
        if (val === '' || val === undefined) {
          // If empty string or undefined, return undefined
          return undefined;
        } else {
          return new Date(val).toISOString();
        }
      }),
    status: z.enum([
      'NotAssigned',
      'Pending',
      'Scheduled',
      'InTransit',
      'ReadyForSignature',
      'Signed',
      'Corrected',
      'UnderCorrection',
      'MtnValidationFailed',
    ]),
    /**
     * Whether the manifest is publicly available through EPA
     */
    isPublic: z.boolean().optional(),
    generator: handlerSchema.optional(),
    transporters: z.array(transporterSchema),
    wastes: z.array(z.any()),
    designatedFacility: handlerSchema.optional(),
    submissionType: z.enum(['FullElectronic', 'DataImage5Copy', 'Hybrid', 'Image']),
  })
  .refine(
    // Check potential ship date is greater than today if the manifest is still in a pre-shipment phase
    (manifest) => {
      if (manifest.status === 'Pending' || manifest.status === 'NotAssigned') {
        if (manifest.potentialShipDate && new Date(manifest.potentialShipDate) < new Date()) {
          return false;
        }
      }
      return true;
    },
    { path: ['potentialShipDate'], message: 'Date must be after today' }
  )
  .refine(() => {
    // ToDo Validate that if submission Type is FullElectronic, generator.canEsign is true
    return true;
  })
  .refine(
    (manifest) => {
      if (!manifest.generator) {
        return false;
      }
    },
    { path: ['generator'], message: 'Add a Generator for this manifest' }
  )
  .refine(
    (manifest) => {
      if (!manifest.designatedFacility) {
        return false;
      }
    },
    { path: ['designatedFacility'], message: 'Add a designated Facility for this manifest' }
  )
  .refine(
    (manifest) => {
      if (manifest.wastes.length < 1) {
        return false;
      }
    },
    { path: ['wastes'], message: 'At least 1 wasteline is required' }
  )
  .refine(
    (manifest) => {
      if (manifest.transporters.length < 1) {
        return false;
      }
    },
    { path: ['transporters'], message: 'At least 1 transporter is required' }
  );

const rejectionInfoSchema = z.object({
  rejectionType: z.enum(['FullRejection', 'PartialRejection']),
  alternateDesignatedFacilityType: z.enum(['Generator', 'Tsdf']),
  // generatorPaperSignature: ???
  // generatorElectronicSignature: ???
  alternateDesignatedFacility: rcraSite, // ToDo this should be a handler
  newManifestTrackingNumber: z.string(),
  rejectionComments: z.string(),
});

/**
 * The Manifest, also known as hazardous waste manifest, is a key component of the
 * United States Environmental Protection Agency's (US EPA) hazardous waste tracking
 * program. It captures information on the type and quantity of waste being transported,
 * instructions for handling, and custody exchange data (signatures).
 */
export type Manifest = z.infer<typeof manifestSchema>;
export type RejectionInfo = z.infer<typeof rejectionInfoSchema>;