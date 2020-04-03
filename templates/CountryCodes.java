import javax.annotation.Generated;

/**
 * Enumeration containing different country codes in ISO 3166.
 *
 * Values are:
 * - ISO3166-1-Alpha-2
 * - ISO3166-1-Alpha-3
 * - ISO3166-1-numeric
 */
@Generated(value = "$GENERATOR_NAME$", date = "$GENERATION_DATE$")
public enum CountryCodes {

    // @formatter:off
    $ENUM_VALUES$
    // @formatter:on

    private String name;
    private String alpha2;
    private String alpha3;
    private int numeric;

    /**
     * Returns the country name
     *
     * @return The alphanumeric value, 2 characters
     */
    public String getName() {
        return name;
    }

    /**
     * Returns the alphanumeric value, 2 characters
     *
     * @return The alphanumeric value, 2 characters
     */
    public String getAlpha2() {
        return alpha2;
    }

    /**
     * Returns the alphanumeric value, 3 characters
     *
     * @return The alphanumeric value, 3 characters
     */
    public String getAlpha3() {
        return alpha3;
    }

    /**
     * Returns the numeric value
     *
     * @return The numeric value
     */
    public int getNumeric() {
        return numeric;
    }

    /**
     * Constructor
     *
     * @param name The country name
     * @param alpha2 The alphanumeric value, 2 characters
     * @param alpha3 The alphanumeric value, 3 characters
     * @param numeric The numeric value
     */
    CountryCodes(String name, String alpha2, String alpha3, int numeric) {
        this.name = name;
        this.alpha2 = alpha2;
        this.alpha3 = alpha3;
        this.numeric = numeric;
    }
}
